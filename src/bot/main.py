from client import Client

bot = Client(token = "NzQwNTY4NzY2MTk4NDQ4MTkw.Xyq6aA.ryjwwbMeF8rUnjBJwZiLP3_uaAk")

@bot.command()
async def test(ctx):
	player = bot.lavalink.player_manager.get(ctx.guild.id)

	await ctx.send(str(player.current))

bot.initiate()