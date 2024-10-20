
import asyncio
import click

from k8spython.models import ServiceConfig
from k8spython.service.web import webservice_start
from pydantic_yaml import parse_yaml_raw_as, to_yaml_str




def config_parse(config_file: click.File) -> ServiceConfig:
    """
    Read and parse the configuration file
    """

    click.echo(f"Starting service with config file: {config_file}")

    config = parse_yaml_raw_as(ServiceConfig, config_file)

    click.secho("Config:", fg="green")
    click.echo(to_yaml_str(config))

    return config



def service_start(config_file: click.File):
    """
    Start the service with the given configuration file
    """

    config = config_parse(config_file)

    click.secho(f"Starting service:", fg="green")

    # asyncio.run(start_webservice(config))
    webservice_start(config)

    click.secho(f"Service stopped", fg="red")
