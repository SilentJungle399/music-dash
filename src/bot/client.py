from discord.ext import commands
import discord
import logging, coloredlogs, sockevents, lavaclient, base64, lavalink
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

		super().__init__(command_prefix='?', token = token, intents = intents)

		self.sessions = {}

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

	def initiate(self):
		self.run(self.token)

	async def on_ready(self):
		logging.info(f"Logged in as {self.user}")
		
		await web._run_app(self.app, port=3000)

	async def playPlayer(self, data):
		player = self.lavalink.player_manager.get(int(data["server_id"]))
		if not player:
			player = self.lavalink.player_manager.create(int(data["server_id"]), endpoint=str("india"))
		guild = self.get_guild(int(data['server_id']))
		if not player.is_connected:
			ch = (guild.get_member(int(data["user_id"]))).voice.channel
			await self.get_guild(int(data["server_id"])).change_voice_state(channel=ch)
		results = await player.node.get_tracks(data["song"])
		tracka = results['tracks'][0]
		track = lavalink.models.AudioTrack(tracka, int(data["user_id"]), recommended=True)
		player.add(requester=int(data["user_id"]), track=track)
		queue = []
		for i in player.queue:
			queue.append(await self.gettrackdata(player, i))

		ret = []
		if len(ch.members) > 1:
			for i in ch.members:
				ret.append(str(i.id))
		await self.socket.emit("newQueue", {
			"queue": queue,
			"members": ret
		})

		if not player.is_playing:
			await player.play()

	async def get_tracks(self, data):
		player = self.lavalink.player_manager.get(int(data["server_id"]))
		results = await player.node.get_tracks(f'ytsearch:{data["song"]}')
		return results["tracks"]

	async def gettrackdata(self, player, track):
		return {
			"raw": self.getrawtrack(track),
			"name": track.title,  			 	# track name
			"url": track.uri, 				    # yt url
			"duration": int(track.duration),		# track duration - integer
			"channel": track.author,				# yt channel
			"position": int(player.position)	# position timestamp - integer
		}

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

	async def stopPlayer(self, player):
		channel = self.get_channel(int(player.channel_id))
		if len(channel.members) > 1:
			ret = []
			for i in channel.members:
				ret.append(str(i.id))

			await player.stop()
			player.queue = []
			await self.socket.emit("newStop", {
				"members": ret
			})

	async def pausePlayer(self, player, boolean):
		channel = self.get_channel(int(player.channel_id))
		await player.set_pause(boolean)
		if len(channel.members) > 1:
			ret = []
			for i in channel.members:
				ret.append(str(i.id))
			await self.socket.emit("newPause", {
				"members": ret,
				"pause": boolean
			})

	async def seekPlayer(self, data):
		player = self.lavalink.player_manager.get(int(data['server_id']))
		channel = self.get_channel(int(player.channel_id))
		if len(channel.members) > 1:
			ret = []
			for i in channel.members:
				ret.append(str(i.id))
			
			await player.set_pause(True)
			await player.seek(int(data['seek']))
			await player.set_pause(False)
			await self.socket.emit("newSeek", {
				"members": ret,
				"seek": data['seek']
			})

	
	async def on_voice_state_update(self, member, before, after):
		if not after.channel:
			vc = None
			guild = None
		else:
			vc = {
				"name": after.channel.name,
				"id": str(after.channel.id)
			}
			guild = {
				"name": after.channel.guild.name,
				"id": str(after.channel.guild.id),
				"icon": str(after.channel.guild.icon_url)
			}
		await self.socket.emit("newVoiceState", {
			"member": str(member.id),
			"vc": vc,
			"guild": guild
		})