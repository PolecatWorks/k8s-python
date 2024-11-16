#!/usr/bin/env python

# k8spython Copyright (C) 2024 Ben Greene
"""CLI initiated python app
"""

import click
import sys

from .config import ServiceConfig



# https://stackoverflow.com/questions/242485/starting-python-debugger-automatically-on-error
def interactivedebugger(type, value, tb):
    if hasattr(sys, "ps1") or not sys.stderr.isatty():
        # we are in interactive mode or we don't have a tty-like
        # device, so we call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback
        import pdb

        # we are NOT in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print
        # ...then start the debugger in post-mortem mode.
        # pdb.pm() # deprecated
        pdb.post_mortem(tb)  # more "modern"


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    """
    Service and tools for basic service
    """
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug

    if debug:
        click.echo(f"Debug mode is {'on' if debug else 'off'}", err=True)
        sys.excepthook = interactivedebugger


# ------------- CLI commands go below here -------------

from k8spython.config import ServiceConfig


@cli.command()
@click.argument("config_file", type=click.File("rb"))
@click.argument("embed_file", type=click.File("rb"), nargs=-1)
@click.pass_context
def embed(ctx, config_file: click.File, embed_file: click.File):
    """Load a file into the chromadb as an embedding"""
    from .chroma import embed

    from pydantic_yaml import parse_yaml_raw_as, to_yaml_str

    config: ServiceConfig = ServiceConfig(_secrets_dir="secrets")


    config: ServiceConfig = parse_yaml_raw_as(ServiceConfig, config_file)

    embed(embed_file)



@cli.command()
@click.argument("config_file", type=click.File("rb"))
@click.option("--secrets", required=True,type=click.Path(exists=True))
@click.pass_context
def parse(ctx, config_file, secrets):
    """Parse a config"""
    from pydantic_yaml import parse_yaml_raw_as, to_yaml_str


    # config: ServiceConfig = parse_yaml_raw_as(ServiceConfig, config_file)
    config: ServiceConfig = ServiceConfig.from_yaml(config_file.name, secrets)
    click.echo(config)

    click.secho("Config:", fg="green")
    click.echo(to_yaml_str(config))


@cli.command()
@click.option("--config", type=click.File("rb"))
@click.option("--secrets", type=click.Path(exists=True))
@click.pass_context
def start(ctx, config, secrets):
    """Start the service"""

    from k8spython.service import service_start

    service_start(config)



# ------------- CLI commands above here -------------

if __name__ == "__main__":
    cli()
