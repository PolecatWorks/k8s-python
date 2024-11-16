#!/usr/bin/env python

# k8spython Copyright (C) 2024 Ben Greene
"""CLI initiated python app
"""

import click
import sys

from typing import List

from .config import ServiceConfig

from . import chroma



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

def chroma_options(function):
    function = click.option("--config", required=True, type=click.File("rb"))(function)
    function = click.option("--secrets", required=True, type=click.Path(exists=True))(function)
    function = click.pass_context(function)
    return function


@cli.command()
@chroma_options
def parse(ctx, config, secrets):
    """Parse a config"""
    from pydantic_yaml import to_yaml_str

    configObj: ServiceConfig = ServiceConfig.from_yaml(config.name, secrets)
    click.echo(configObj)

    click.echo(to_yaml_str(configObj))


@cli.command()
@chroma_options
@click.argument("embed_files", type=click.File("rb"), nargs=-1)
def embed(ctx, config: click.File, secrets: click.Path, embed_files: List[click.File]):
    """Load a file into the chromadb as an embedding"""

    configObj: ServiceConfig = ServiceConfig.from_yaml(config.name, secrets)

    results = chroma.embed(configObj.chroma, "splat", embed_files)

    for count, id in enumerate(results):
        click.echo(f'Embedded [{count}]: {id}')


@cli.command()
@chroma_options
@click.argument("text", type=click.STRING)
def query(ctx, config: click.File, secrets: click.Path, text: str):
    """Query for some text against the collection"""

    configObj: ServiceConfig = ServiceConfig.from_yaml(config.name, secrets)

    results = chroma.query(configObj.chroma, "splat", text, 2)

    click.echo(results)


    # stophere



@cli.command()
@chroma_options
def start(ctx, config, secrets):
    """Start the service"""
    from k8spython.service import service_start

    configObj: ServiceConfig = ServiceConfig.from_yaml(config.name, secrets)

    service_start(configObj)





# ------------- CLI commands above here -------------

if __name__ == "__main__":
    cli()
