
import asyncio
import click

from k8spython.hams import hams_app_create
from k8spython.config import ServiceConfig
from k8spython.service.web import AppleView
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str
from aiohttp import web




def config_parse(config_file: click.File) -> ServiceConfig:
    """
    Read and parse the configuration file
    """

    config = parse_yaml_raw_as(ServiceConfig, config_file)

    click.secho("Config:", fg="green")
    click.echo(to_yaml_str(config))

    return config


def service_app_create(app: web.Application, config: ServiceConfig) -> web.Application:
    """
    Create the service with the given configuration file
    """

    app['config'] = config
    app.router.add_get(f'/{config.webservice.prefix}/apple', AppleView)

    # TODO: https://docs.aiohttp.org/en/stable/web_reference.html#aiohttp.web.AppKey
    app['webservice'] = app

    click.secho(f"Service: { {app['config'].webservice.url.host}}:{app['config'].webservice.url.port}/{app['config'].webservice.prefix}", fg="green")

    return app


def service_init(app: web.Application, config_file: click.File):
    config = config_parse(config_file)

    service_app_create(app, config)
    hams_app_create(app, config.hams)
    return app


def service_start(config_file: click.File):
    """
    Start the service with the given configuration file
    """
    app = web.Application()

    service_init(app, config_file)



    web.run_app(app, host=app['config'].webservice.url.host, port=app['config'].webservice.url.port)

    click.secho(f"Service stopped", fg="red")
