import lavalink, logging
from classes import Session
from classes import CustomPlayer

class LavaClient(lavalink.Client):
	def __init__(self, bot):
		super().__init__(bot.user_id, player=CustomPlayer)
		
		self.bot = bot

		self.add_node(
			"localhost",
			2333,
			"youshallnotpass",
			"in",
		)

		self.bot.add_listener(self.voice_update_handler, 'on_socket_response')
		self.add_event_hook(self.track_hook)

	async def track_hook(self, event):
		logging.info(str(event))
		if isinstance(event, lavalink.events.TrackStartEvent):
			event: lavalink.events.TrackStartEvent = event
			channel = self.bot.get_channel(int(event.player.channel_id)) if event.player.channel_id else event.player.channel

			for i in channel.members:
				session: Session = self.bot.sessions.get(str(i.id))

				if session:
					await self.bot.socket.emit('TrackStart', {
						"track": self.bot.getrawtrack(event.track),
					}, to = session["socketid"])

		elif isinstance(event, lavalink.events.TrackEndEvent):
			channel = self.bot.get_channel(int(event.player.channel_id))

			for i in channel.members:
				session: Session = self.bot.sessions.get(str(i.id))

				if session:
					await self.bot.socket.emit('TrackEnd', {}, to = session["socketid"])