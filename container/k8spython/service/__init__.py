
import asyncio
import logging

from k8spython.service.state import Events
from k8spython.hams import hams_app_create
from k8spython.config import ServiceConfig
from k8spython.service.web import AppleView, ChunkView
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str
from aiohttp import web
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


async def service_coroutine(app: web.Application):
    """
    Coroutine for the service
    """
    logger.info("Service: coroutine start")

    eventState = Events(app['config'].events, datetime.now(timezone.utc), 0)

    app['events'] = eventState

    while True:
        waitTime = eventState.updateChunk(datetime.now(timezone.utc))

        await asyncio.sleep(waitTime)


async def service_coroutine_cleanup(app: web.Application):
    """
    Launch the coroutine as a cleanup task
    """

    app['coroutine'] = asyncio.create_task(service_coroutine(app))


    logger.info("Service: coroutine running")
    yield

    app['coroutine'].cancel()

    logger.info("Service: coroutine cleanup")


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

    logger.info(f"Service: {app['config'].webservice.url.host}:{app['config'].webservice.url.port}/{app['config'].webservice.prefix}")

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


    web.run_app(app, host=app['config'].webservice.url.host, port=app['config'].webservice.url.port,
                access_log_format='%a "%r" %s %b "%{Referer}i" "%{User-Agent}i"',
                access_log=logger)

    logger.info(f"Service stopped")
