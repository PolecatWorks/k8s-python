from aiohttp import web



def webservice_start(config):
    """
    Start the web service
    """
    app = web.Application()

    app['config'] = config
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    web.run_app(app)


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
