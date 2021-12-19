from typing import Dict
from discord.ext import commands
import discord
import logging, coloredlogs, sockevents, lavaclient, base64, lavalink, asyncio, time
from classes import Session
from lavalink.models import DefaultPlayer
from aiohttp import web

coloredlogs.install(
	fmt = '%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%d-%b-%y %H:%M:%S',
	level = logging.INFO
)

class Client(commands.Bot):
	def __init__(self, token = None):
		self.token = token
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
			],
		)

		self.app = web.Application()
		aiologger = logging.getLogger('aiohttp.access')
		aiologger.setLevel(logging.CRITICAL)

		self.socket.attach(self.app)
		self.loop.create_task(self.sync_positions())

	def initiate(self):
		self.run(self.token)

	async def on_ready(self):
		logging.info(f"Logged in as {self.user}")
		
		await web._run_app(self.app, port=3000)

	async def sync_positions(self):
		while True:
			for i in self.sessions:
				i = self.sessions[i]
				player: DefaultPlayer = self.lavalink.player_manager.get(int(i["guild"]["id"]))
				channel = self.get_channel(int(i["voice"]["id"]))
				
				if player.current and player.channel_id and channel.id == int(player.channel_id):
					increase = player.position*100/player.current.duration

					await self.socket.emit("updatePosition", {
						"position": increase,
					}, to = i["socketid"])

					print(increase)
				
			await asyncio.sleep(0.5)

	async def on_voice_state_update(self, member, before, after):
		if member.id == self.user_id:
			return
		
		if after.channel is None:
			return

		player = self.lavalink.player_manager.get(int(after.channel.guild.id))
		uses = self.sessions.get(str(member.id))
		if uses:
			if not after.channel:
				self.sessions.pop(str(member.id))
			else:
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

		if after.channel and player.channel_id == after.channel.id:
			for i in after.channel.members:
				session = self.sessions.get(str(i.id))
				await self.socket.emit("newMemberJoin", {
					"id": str(i.id),
					"name": str(i.name),
					"pfp": str(i.avatar_url),
					"discrim": str(i.discriminator),
				}, to = session["socketid"])
		elif not after.channel or (before.channel and player.channel_id == before.channel.id):
			for i in before.channel.members:
				session = self.sessions.get(str(i.id))
				await self.socket.emit("newMemberLeave", {
					"id": str(i.id),
					"name": str(i.name),
					"pfp": str(i.avatar_url),
					"discrim": str(i.discriminator),
				}, to = session["socketid"])

	def getrawtrack(self, track):
		return {
			"track": track.track,
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