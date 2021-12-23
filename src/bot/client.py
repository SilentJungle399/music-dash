from typing import Dict
from aiohttp.web_request import Request
from discord.ext import commands
import logging, coloredlogs, sockevents, lavaclient, base64, asyncio, discord
from classes import OAuth, Session
from lavalink.models import DefaultPlayer
from aiohttp import web

coloredlogs.install(
	fmt = '%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%d-%b-%y %H:%M:%S',
	level = logging.INFO
)

class Client(commands.Bot):
	def __init__(self, token = None, client_id = None, client_secret = None, redirect_uri = None, **options):
		self.token = token
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri

		if not self.token:
			self.token = input("Enter your bot token: ")
		
		token_part0 = self.token.partition('.')[0].encode()
		self.user_id = int(base64.b64decode(token_part0 + b'=' * (3 - len(token_part0) % 3)))

		intents = discord.Intents.default()
		intents.members = True

		super().__init__(command_prefix='!', token = token, intents = intents)

		self.load_extension("jishaku")

		self.sessions: Dict[str, Session] = {}

		self.lavalink = lavaclient.LavaClient(self)

		self.socket = sockevents.Server(
			bot = self,
			reconnection = True, 
			reconnection_attempts = 0, 
			reconnection_delay = 2,
			cors_allowed_origins = [
				"http://localhost:8080",
				"http://vps.silentjungle.tk:8080"
			],
		)

		self.app = web.Application()	
		aiologger = logging.getLogger('aiohttp.access')
		aiologger.setLevel(logging.CRITICAL)

		routes = [
			web.get('/callback', self.handle_oauth),
		]

		if not options.get("dev"):
			routes.extend([
				web.get('/', self.send_html),
				web.static("/js", "dist/js"),
				web.static("/css", "dist/css"),
				web.static("/favicon.ico", "dist")
			])

		self.app.add_routes(routes)

		self.socket.attach(self.app)
		self.loop.create_task(self.sync_positions())

	async def send_html(self, r):
		with open("dist/index.html", "r") as f:
			return web.Response(text = f.read(), content_type='text/html')

	def initiate(self):
		self.run(self.token)

	async def on_ready(self):
		logging.info(f"Logged in as {self.user}")
		
		await web._run_app(self.app, port=3000)

	async def handle_oauth(self, request: Request):
		code = request.query.get("code")
		if not code:
			return web.Response(status=400)

		oauth = OAuth(
			client_id = self.client_id,
			client_secret = self.client_secret,
			redirect_uri = self.redirect_uri,
			bot = self
		)

		token = await oauth.get_token(code)
		user = await oauth.get_user(token)

		resp = web.HTTPSeeOther(location="/")

		resp.set_cookie("token", token["refresh_token"])

		return resp

	async def sync_positions(self):
		while True:
			for i in self.sessions:
				i = self.sessions[i]
				if not i["voice"]["id"]:
					continue

				player: DefaultPlayer = self.lavalink.player_manager.get(int(i["guild"]["id"]))
				channel = self.get_channel(int(i["voice"]["id"]))
				
				if player.current and player.channel_id and channel.id == int(player.channel_id):
					increase = player.position*100/player.current.duration

					await self.socket.emit("updatePosition", {
						"position": increase,
					}, to = i["socketid"])

			await asyncio.sleep(0.5)

	async def sync_queue(self, player, channel):
		queue = []
		for track in player.queue:
			queue.append(self.getrawtrack(track))

		for i in channel.members:
			session = self.sessions.get(str(i.id))
			if session:
				await self.socket.emit('newQueue', {
					"queue": queue,
				}, to = session["socketid"])

	async def on_voice_state_update(self, member, before, after):
		if member.id == self.user_id:
			return

		uses = self.sessions.get(str(member.id))
		if uses:
			self.sessions.pop(str(member.id))
			event = sockevents.Event(
				uses["socketid"], 
				{
					"sid": uses["sid"],
					"user": str(member.id),
				},
				self.socket
			)

			await self.socket.on__verifyUser(event)

		player = self.lavalink.player_manager.get(int(after.channel.guild.id) if after.channel else int(before.channel.guild.id))

		if player and after.channel and player.channel_id == after.channel.id:
			for i in after.channel.members:
				session = self.sessions.get(str(i.id))
				await self.socket.emit("newMemberJoin", {
					"id": str(i.id),
					"name": str(i.name),
					"pfp": str(i.avatar_url),
					"discrim": str(i.discriminator),
				}, to = session["socketid"])
		elif before.channel and before.channel.id == player.channel_id:
			for i in before.channel.members:
				session = self.sessions.get(str(i.id))
				await self.socket.emit("newMemberLeave", {
					"id": str(i.id),
					"name": str(i.name),
					"pfp": str(i.avatar_url),
					"discrim": str(i.discriminator),
				}, to = session["socketid"])

	def getrawtrack(self, track):
		requester = self.get_user(int(track.requester))

		return {
			"track": track.track,
			"requester": {
				"id": str(requester.id),
				"name": str(requester.name),
				"pfp": str(requester.avatar_url),
				"discrim": str(requester.discriminator),
			} if requester else None,
			"info": {
				"identifier": track.identifier,
				"isSeekable": track.is_seekable,
				"author": track.author,
				"length": track.duration,
				"isStream": track.stream,
				"title": track.title,
				"uri": track.uri
			}
		}