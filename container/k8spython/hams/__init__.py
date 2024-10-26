
from aiohttp import web
from k8spython.hams.config import HamsConfig
import click


async def hams_app_cleanup(app: web.Application):
    """
    Cleanup the service
    """
    click.secho("HaMS: Starting", fg="green")
    hams_app = web.Application()
    runner = web.AppRunner(hams_app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8079)

    app['hams'] = hams_app
    await site.start()
    yield

    click.secho("HaMS: Cleaning up", fg='red')
    await runner.cleanup()


def hams_app_create(app: web.Application, config: HamsConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    app.cleanup_ctx.append(hams_app_cleanup)

    # https://docs.aiohttp.org/en/v3.8.4/web_advanced.html#cleanup-context


    return app
