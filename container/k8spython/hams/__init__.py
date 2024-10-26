
from aiohttp import web
from k8spython.hams.config import HamsConfig
import click


async def hams_app_cleanup(app: web.Application):
    """
    Cleanup the service
    """

    click.secho("HaMS: starting", fg="green")
    runner = web.AppRunner(app['hams'].hams_app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8079)

    await site.start()
    yield

    click.secho("HaMS: cleaning up", fg='red')
    await runner.cleanup()


class AliveView(web.View):
    async def get(self):

        hams = self.request.app['hams']
        print(hams.app['config'])
        # print(dir(self.request.app['']))
        alive = {
            "alive": True
        }
        return web.json_response(alive)


class ReadyView(web.View):
    async def get(self):
        return web.Response(text="I'm ready")


class Hams:
    def __init__(self, hams_app: web.Application, app: web.Application, config: HamsConfig):
        self.app = app
        self.hams_app = hams_app
        self.config = config


def hams_app_create(app: web.Application, config: HamsConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    hams_app = web.Application()
    hams = Hams(hams_app, app, config)
    # Provide a ref back to app from HaMS
    hams_app['hams'] = hams
    app['hams'] = hams


    app['hams'].hams_app.router.add_get('/hams/alive', AliveView)
    app['hams'].hams_app.router.add_get('/hams/ready', ReadyView)

    app.cleanup_ctx.append(hams_app_cleanup)

    # https://docs.aiohttp.org/en/v3.8.4/web_advanced.html#cleanup-context
    click.secho(f"HaMS: created", fg="green")

    return app
