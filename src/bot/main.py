from client import Client
import time

bot = Client(token = "ODY1MjE5MDUzNTM0OTY5OTA2.YPA0CQ.eqjogIGLFkkDlJGd92GHCntWOHI")

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

@bot.command()
async def pr(ctx):
	print(bot.sessions)

bot.initiate()