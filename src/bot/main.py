from client import Client
import time

bot = Client(
	token = "NzQwNTY4NzY2MTk4NDQ4MTkw.Xyq6aA.ryjwwbMeF8rUnjBJwZiLP3_uaAk",
	client_id = "740568766198448190",
	client_secret = "50dcrsZdDygQ9rWZjpWzD34jVkjfkW5Y",
	redirect_uri = "http://localhost:8080/callback",
	dev = True
)
# bot = Client(token = "ODY1MjE5MDUzNTM0OTY5OTA2.YPA0CQ.eqjogIGLFkkDlJGd92GHCntWOHI")

@bot.command()
async def ping(ctx):
	t1 = time.monotonic()
	await ctx.trigger_typing()

	t2 = time.monotonic()

	await ctx.send(f"Pong! `{round((t2 - t1) * 1000)}ms`")

bot.initiate()