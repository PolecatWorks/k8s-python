
import asyncio
import click

from k8spython.service.state import Events
from k8spython.hams import hams_app_create
from k8spython.config import ServiceConfig
from k8spython.service.web import AppleView, ChunkView
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str
from aiohttp import web
from datetime import datetime, timezone


async def service_coroutine(app: web.Application):
    """
    Coroutine for the service
    """
    click.secho("Service: coroutine start", fg='red')


    click.echo("OK")
    eventState = Events(app['config'].events, datetime.now(timezone.utc), 5)
    click.echo("O2K")

    app['events'] = eventState

    click.secho(f"BLOOP: {eventState}", fg="yellow", bg="blue")

    while True:
        waitTime = eventState.updateChunk(datetime.now(timezone.utc))
        # click.secho(f"Service: coroutine running {waitTime}", fg='red')

        await asyncio.sleep(waitTime)


async def service_coroutine_cleanup(app: web.Application):
    """
    Launch the coroutine as a cleanup task
    """
    # click.secho("Service: coroutine start", fg='red')

    app['coroutine'] = asyncio.create_task(service_coroutine(app))


    click.secho("Service: coroutine running", fg='red')
    yield

    app['coroutine'].cancel()

    click.secho("Service: coroutine cleanup", fg='red')


def service_app_create(app: web.Application, config: ServiceConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    app['config'] = config


    app.cleanup_ctx.append(service_coroutine_cleanup)

    app.router.add_get(f'/{config.webservice.prefix}/apple', AppleView)
    app.add_routes([web.view(f'/{config.webservice.prefix}/chunks', ChunkView)])

    # TODO: https://docs.aiohttp.org/en/stable/web_reference.html#aiohttp.web.AppKey
    app['webservice'] = app

    click.secho(f"Service: {app['config'].webservice.url.host}:{app['config'].webservice.url.port}/{app['config'].webservice.prefix}", fg="green")

    return app


def service_init(app: web.Application, config: ServiceConfig):


    service_app_create(app, config)
    hams_app_create(app, config.hams)
    return app


def service_start(config: ServiceConfig):
    """
    Start the service with the given configuration file
    """
    app = web.Application()

    service_init(app, config)


    web.run_app(app, host=app['config'].webservice.url.host, port=app['config'].webservice.url.port)

    click.secho(f"Service stopped", fg="red")
