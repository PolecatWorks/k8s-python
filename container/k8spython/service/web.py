from aiohttp import web



class AppleView(web.View):
    async def get(self):
        return web.Response(text="Apple")
