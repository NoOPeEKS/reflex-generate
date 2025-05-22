"""Reflex-Generate CLI to create HTTP Resources for Reflex apps."""

import sys
from importlib import metadata
from importlib.util import find_spec

import click


def check_dependencies():
    """Checks if reflex is installed as a dependency."""
    if not find_spec("reflex"):
        sys.stdout.write("You must have `reflex` installed before using this app\n")
        exit(1)


@click.group()
@click.version_option(metadata.version("reflex-generate"), message="%(version)s")
def cli():
    """Reflex-Generate CLI to create HTTP Resources for Reflex apps."""
    check_dependencies()
    pass


@cli.command()
@click.argument("model_name", nargs=1)
@click.argument("fields", nargs=-1)
def scaffold(model_name: str, fields: tuple[str, ...]):
    """Subcommand for managing the scaffolding of resources."""
    pass


if __name__ == "__main__":
    cli()
