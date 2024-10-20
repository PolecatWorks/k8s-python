from aiohttp import web



def webservice_init(app: web.Application)-> web.Application:
    """
    Start the web service
    """

    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    return app


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
