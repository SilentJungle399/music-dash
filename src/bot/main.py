from client import Client
import time

bot = Client(token = "NzQwNTY4NzY2MTk4NDQ4MTkw.Xyq6aA.ryjwwbMeF8rUnjBJwZiLP3_uaAk")

@bot.command()
async def test(ctx):
	player = bot.lavalink.player_manager.get(ctx.guild.id)

	await ctx.send(str(player.current))

@bot.command()
async def ping(ctx):
	t1 = time.monotonic()
	await ctx.trigger_typing()

	t2 = time.monotonic()

	await ctx.send(f"Pong! `{round((t2 - t1) * 1000)}ms`")

bot.initiate()