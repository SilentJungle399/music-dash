import discord
import socketio, logging, json, lavalink

class Event:
	def __init__(self, sid, data, socket: 'Server'):
		self.sid = sid
		self.data = data
		self.socket = socket

	async def reply(self, event, data):
		await self.socket.emit(event, data, to=self.sid)

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
						player: lavalink.DefaultPlayer = self.bot.lavalink.player_manager.get(guild.id)
						if not player:
							player = self.bot.lavalink.player_manager.create(guild.id)
							player.store('channel', member.voice.channel.id)
							cursong = player.current
							if cursong:
								retsong = await self.bot.gettrackdata(player, cursong)
							else:
								retsong = None
							queue = []
							for song in player.queue:
								queue.append(await self.bot.gettrackdata(player, song))

						else:
							retsong = None
							queue = []

						self.bot.sessions[event.data['user']] = {
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
								"position": player.position,
							},
							"voice": {
								"channel": {
									"id": member.voice.channel.id,
									"name": member.voice.channel.name,
								},
								"guild": {
									"id": guild.id,
									"name": guild.name,
									"icon": "https://cdn.discordapp.com" + str(guild.icon_url._url),
								},
							}
						})
						
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
				"position": 0,
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