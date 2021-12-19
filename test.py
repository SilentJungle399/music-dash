import aiohttp
import asyncio

CLIENT_ID = "740568766198448190"
CLIENT_SECRET = "50dcrsZdDygQ9rWZjpWzD34jVkjfkW5Y"
REDIRECT_URI = "http://silentjungle.tk/callback"
code = "CjlGPgfMsn2ES7B2DMJYUdeEKT2vTs"

async def gettoken():

	data = {
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': REDIRECT_URI
	}

	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	client = aiohttp.ClientSession()
	req = await client.post('https://discord.com/api/v8/oauth2/token', data=data, headers = headers)

	return await req.json()

async def newtoken(retdata):
	data = {
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': 'refresh_token',
		'refresh_token': retdata['refresh_token'],
	}

	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	client = aiohttp.ClientSession()
	req = await client.post('https://discord.com/api/v8/oauth2/token', data=data, headers = headers)

	return await req.json()

async def useaccess(retdata):
	headers = {
		'Authorization': retdata['token_type'] + " " + retdata['access_token']
	}
	print(headers)

	client = aiohttp.ClientSession()
	req = await client.get('https://discord.com/api/v8/users/@me', headers = headers)

	print(req.status)
	print("------------------")
	print(await req.text())
	print("------------------")
	print(await req.json())

async def do():
	# data = await gettoken()
	# print(data)
	data = await newtoken({
		"refresh_token": "iWV5fcNmPdKVRmjDIXV7bOH0pGps77"
	})
	print(data)

	a = await useaccess(data)
	print(a)

asyncio.run(do())