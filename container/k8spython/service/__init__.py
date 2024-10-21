
import asyncio
import click

from k8spython.models import ServiceConfig
from k8spython.service.web import webservice_init
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


def service_app_create(config_file: click.File) -> web.Application:
    """
    Create the service with the given configuration file
    """

    config = config_parse(config_file)

    app = web.Application()
    app['config'] = config
    app['webservice'] = webservice_init(app)


    click.secho(f"Service created", fg="green")
    return app


def service_start(config_file: click.File):
    """
    Start the service with the given configuration file
    """

    app = service_app_create(config_file)
    web.run_app(app, host=app['config'].webservice.url.host, port=app['config'].webservice.url.port)



    click.secho(f"Service stopped", fg="red")
