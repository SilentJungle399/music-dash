import lavalink, logging

class LavaClient(lavalink.Client):
	def __init__(self, bot):
		super().__init__(bot.user_id)
		
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
		logging.info(event)