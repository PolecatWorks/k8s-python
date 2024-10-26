
from aiohttp import web
from k8spython.hams.config import HamsConfig
import click


async def hams_app_cleanup(app: web.Application):
    """
    Cleanup the service
    """

    click.secho("HaMS: starting", fg="green")
    runner = web.AppRunner(app['hams'])
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8079)

    await site.start()
    yield

    click.secho("HaMS: cleaning up", fg='red')
    await runner.cleanup()


class AliveView(web.View):
    async def get(self):
        return web.Response(text="I'm alive")

class ReadyView(web.View):
    async def get(self):
        return web.Response(text="I'm ready")


def hams_app_create(app: web.Application, config: HamsConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    app['hams'] = web.Application()

    app['hams'].router.add_get('/hams/alive', AliveView)
    app['hams'].router.add_get('/hams/ready', ReadyView)

    app.cleanup_ctx.append(hams_app_cleanup)

    # https://docs.aiohttp.org/en/v3.8.4/web_advanced.html#cleanup-context
    click.secho(f"HaMS: created", fg="green")

    return app
