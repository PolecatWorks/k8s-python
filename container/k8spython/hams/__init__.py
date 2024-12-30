from aiohttp import web
from k8spython.hams.config import HamsConfig
import logging
from k8spython import keys
import signal
import asyncio
from prometheus_async import aio

# Set up logging
logger = logging.getLogger(__name__)


def shutdownSig():
    logger.info("Sending SIGTERM")
    signal.raise_signal(signal.SIGTERM)


async def hams_app_cleanup(app: web.Application):
    """
    Cleanup the service
    """

    runner = web.AppRunner(
        app[keys.hams].hams_app,
        access_log_format='%a "%r" %s %b "%{Referer}i" "%{User-Agent}i"',
        access_log=logger,
    )
    await runner.setup()
    site = web.TCPSite(
        runner, app[keys.hams].config.url.host, app[keys.hams].config.url.port
    )

    await site.start()

    logger.info("Executing startup scripts")
    logger.debug(f"prestart = {app[keys.config].hams.checks}")
    await app[keys.config].hams.checks.run_preflights()

    yield

    logger.info("HaMS: cleaning up")
    await app[keys.config].hams.checks.run_shutdowns()
    await runner.cleanup()


class AliveView(web.View):
    async def get(self):

        hams = self.request.app[keys.hams]

        reply = hams.alive()
        alive = {"alive": reply}
        return web.json_response(alive, status=200 if reply else 503)


class ReadyView(web.View):
    async def get(self):
        hams: Hams = self.request.app[keys.hams]

        reply = hams.ready()
        ready = {"ready": reply}
        return web.json_response(ready, status=200 if reply else 503)


class MonitorView(web.View):
    async def get(self):
        ready = {"monitor": True}
        return web.json_response(ready, status=200)


class ShutdownView(web.View):
    async def post(self):

        ready = {"shutdown": True}
        hams: Hams = self.request.app[keys.hams]

        logger.info(
            "Shutting down stall for conneciton draiining. Ready will be disabled automatically by k8s"
        )

        waitTime = self.request.app[keys.hams].config.shutdownDuration.total_seconds()
        await asyncio.sleep(waitTime)

        return web.json_response(ready, status=200)


class Hams:
    def __init__(
        self, hams_app: web.Application, app: web.Application, config: HamsConfig
    ):
        self.app = app
        self.hams_app = hams_app
        self.config = config

    def alive(self) -> bool:
        return True

    def ready(self) -> bool:
        return self.app[keys.events].spareCapacity()


def hams_app_create(base_app: web.Application, config: HamsConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    app = web.Application()
    hams = Hams(app, base_app, config)
    # Provide a ref back to app from HaMS
    app[keys.hams] = hams
    base_app[keys.hams] = hams

    logger.info(
        f"HaMS: {hams.config.url.host}:{hams.config.url.port}/{hams.config.prefix}"
    )

    app.add_routes(
        [
            web.view(f"/{hams.config.prefix}/alive", AliveView),
            web.view(f"/{hams.config.prefix}/ready", ReadyView),
            web.view(f"/{hams.config.prefix}/monitor", MonitorView),
            web.view(f"/{hams.config.prefix}/metrics", aio.web.server_stats),
            web.view(f"/{hams.config.prefix}/shutdown", ShutdownView),
        ]
    )

    base_app.cleanup_ctx.append(hams_app_cleanup)

    # https://docs.aiohttp.org/en/v3.8.4/web_advanced.html#cleanup-context

    return base_app
