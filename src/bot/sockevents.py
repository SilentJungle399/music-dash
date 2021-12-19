from lavalink.models import DefaultPlayer
import socketio, logging, json, lavalink, discord, asyncio

class Event:
	def __init__(self, sid, data, socket: 'Server'):
		self.sid = sid
		self.data = data
		self.socket = socket

	async def reply(self, event, data):
		await self.socket.emit(event, data, to=self.sid)

	def __repr__(self) -> str:
		return f"<Event sid={self.sid} data={self.data}>"

	def __str__(self) -> str:
		return self.__repr__()

class Server(socketio.AsyncServer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.bot = kwargs.get('bot')
		self.events = {}

		self.setup_events()
		self.on("*", self.on_event)
		self.on("connect", self.pre__connect)
		self.on("disconnect", self.pre__disconnect)

	def setup_events(self):
		for i in dir(self):
			if i.startswith('on__'):
				self.events[i.strip('on__')] = getattr(self, i)
				logging.info('setup event: {}'.format(i.strip('on__')))

	def log(self, event, data):
		logging.info(event + ": " + (json.dumps(data) if isinstance(data, dict) else data))

	async def on_event(self, event, sid, data):
		ret = Event(sid, data, self)
		await self.events[event](ret)

	async def pre__connect(self, sid, environ):
		self.log('Connected client', sid)

	async def pre__disconnect(self, sid):
		self.log('Disconnected client', sid)

	async def on__seek(self, event: Event):
		self.log('Seek', event.data)
		player: DefaultPlayer = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			return

		pos = event.data["progress"]*player.current.duration/100

		await player.seek(pos)

	async def on__searchSong(self, event: Event):
		self.log('Searching song', event.data)
		player = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			player = self.bot.lavalink.player_manager.create(int(event.data["guild"]["id"]))

		songs = await player.node.get_tracks("ytsearch:"+str(event.data["song"]))

		await event.reply('songResult', {
			"songs": songs['tracks'],
			"keyword": event.data["song"]
		})

	async def on__FastForwardReq(self, event: Event):
		self.log('Fast forward request', event.data)
		player: DefaultPlayer = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			return

		await player.seek(player.position + event.data["ff"]*1000)

	async def on__PlayPauseReq(self, event: Event):
		self.log('Play/Pause request', event.data)
		player: DefaultPlayer = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			return

		await player.set_pause(event.data["state"])

		channel = self.bot.get_channel(int(event.data["channel"]["id"]))
		user = self.bot.get_user(int(event.data["user"]))
		user: discord.User = user if user else (await self.bot.fetch_user(int(event.data["user"])))
		
		for i in channel.members:
			session = self.bot.sessions.get(str(i.id))
			if session:
				await self.emit('playPause', {
					"state": event.data["state"],
					"user": str(user.name) + "#" + str(user.discriminator),
				}, to = session["socketid"])

	async def on__playSongReq(self, event: Event):
		self.log('Playing song', event.data)
		player: DefaultPlayer = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			player = self.bot.lavalink.player_manager.create(int(event.data["guild"]["id"]))

		channel = self.bot.get_channel(int(event.data["channel"]["id"]))
		guild = self.bot.get_guild(int(event.data["guild"]["id"]))

		if not player.is_connected:
			await guild.change_voice_state(channel=channel)

		if not player.is_playing:
			await player.play(event.data["song"], channel = channel, guild = guild)
		else:
			player.add(track = event.data["song"], requester = event.data["user"])

		queue = []
		for track in player.queue:
			queue.append(self.bot.getrawtrack(track))

		for i in channel.members:
			session = self.bot.sessions.get(str(i.id))
			if session:
				await self.emit('newQueue', {
					"queue": queue,
				}, to = session["socketid"])

	async def on__removeSong(self, event: Event):
		self.log('Removing song', event.data)
		player: DefaultPlayer = self.bot.lavalink.player_manager.get(int(event.data["guild"]["id"]))
		if not player:
			return

		player.queue.pop(event.data["song"])

		channel = self.bot.get_channel(int(event.data["channel"]["id"]))
		
		await self.bot.sync_queue(player, channel)

	async def on__verifyUser(self, event: Event):
		self.log('Verify user', event.data)
		user = self.bot.get_user(event.data['user'])
		if not user:
			user = await self.bot.fetch_user(event.data['user'])

		if not user:
			return await event.reply('playerUpdate', {'valid': False})
		else:
			for guild in self.bot.guilds:
				guild: discord.Guild = guild
				member = guild.get_member(user.id)
				if member.voice:
					perms = member.voice.channel.permissions_for(guild.get_member(self.bot.user.id))
					if not (perms.connect and perms.speak):
						return await event.reply('playerUpdate', {
							'valid': True,
							"permissions": False
						})
					else:
						player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(int(guild.id))
						if not player or not player.channel_id:
							player = self.bot.lavalink.player_manager.create(int(guild.id))
							retsong = None
							queue = []
						else:
							channel = guild.get_channel(int(player.channel_id))
							if channel.id != member.voice.channel.id:
								retsong = None
								queue = []
							else:
								cursong = player.current
								if cursong:
									retsong = self.bot.getrawtrack(cursong)
								else:
									retsong = None
								queue = []
								for song in player.queue:
									queue.append(self.bot.getrawtrack(song))

						self.bot.sessions[str(event.data['user'])] = {
							"socketid": event.sid,
							"sid": event.data['sid'],
							"guild": {
								"name": member.guild.name,
								"id": str(member.guild.id),
								"icon": "https://cdn.discordapp.com" + str(guild.icon_url._url)
							},
							"voice": {
								"name": member.voice.channel.name,
								"id": str(member.voice.channel.id)
							}
						}

						return await event.reply('playerUpdate', {
							'valid': True,
							"permissions": True,
							"current": retsong,
							"queue": queue,
							"state": {
								"paused": player.paused,
								"playing": player.is_playing,
								"volume": player.volume,
								"repeat": player.repeat,
								"shuffle": player.shuffle,
								"progress": player.position*100/player.current.duration if player.current else 0
							},
							"voice": {
								"channel": {
									"id": str(member.voice.channel.id),
									"name": member.voice.channel.name,
								},
								"guild": {
									"id": str(guild.id),
									"name": guild.name,
									"icon": "https://cdn.discordapp.com" + str(guild.icon_url._url),
								},
							}
						})
						

		self.bot.sessions[str(event.data['user'])] = {
			"socketid": event.sid,
			"sid": event.data['sid'],
			"guild": {
				"id": None,
				"name": None,
				"icon": None,
			},
			"voice": {
				"id": None,
				"name": None,
			},
		}
		
		return await event.reply("playerUpdate", {
			'valid': True,
			"permissions": True,
			"current": None,
			"queue": [],
			"state": {
				"paused": True,
				"playing": False,
				"volume": 0,
				"repeat": False,
				"shuffle": False,
				"progress": 0,
			},
			"voice": {
				"channel": {
					"id": None,
					"name": None,
				},
				"guild": {
					"id": None,
					"name": None,
					"icon": None,
				},
			}
		})