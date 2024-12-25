import aiohttp


SESSION = None


async def get_global_session():
	global SESSION
	if SESSION is None:
		SESSION = aiohttp.ClientSession()
	return SESSION