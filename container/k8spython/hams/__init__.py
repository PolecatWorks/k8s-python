
from aiohttp import web
from k8spython.hams.config import HamsConfig
import click


async def hams_app_cleanup(app: web.Application):
    """
    Cleanup the service
    """

    click.secho(f"HaMS: starting on {app['hams'].config.url.port} at {app['hams'].config.prefix}", fg="green")
    runner = web.AppRunner(app['hams'].hams_app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', app['hams'].config.url.port)

    await site.start()
    yield

    click.secho("HaMS: cleaning up", fg='red')
    await runner.cleanup()


class AliveView(web.View):
    async def get(self):

        hams = self.request.app['hams']

        reply = hams.alive()
        alive = {
            "alive": reply
        }
        return web.json_response(alive, status=200 if reply else 503)


class ReadyView(web.View):
    async def get(self):
        hams = self.request.app['hams']

        reply = hams.ready()
        ready = {
            "ready": reply
        }
        return web.json_response(ready, status=200 if reply else 503)


class Hams:
    def __init__(self, hams_app: web.Application, app: web.Application, config: HamsConfig):
        self.app = app
        self.hams_app = hams_app
        self.config = config


    def alive(self) -> bool:
        return True


    def ready(self) -> bool:
        return True


def hams_app_create(app: web.Application, config: HamsConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    hams_app = web.Application()
    hams = Hams(hams_app, app, config)
    # Provide a ref back to app from HaMS
    hams_app['hams'] = hams
    app['hams'] = hams



    app['hams'].hams_app.router.add_get(f'/{hams.config.prefix}/alive', AliveView)
    app['hams'].hams_app.router.add_get(f'/{hams.config.prefix}/ready', ReadyView)

    app.cleanup_ctx.append(hams_app_cleanup)

    # https://docs.aiohttp.org/en/v3.8.4/web_advanced.html#cleanup-context
    click.secho(f"HaMS: created", fg="green")

    return app
