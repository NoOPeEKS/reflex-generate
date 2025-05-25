"""Reflex-Generate CLI to create HTTP Resources for Reflex apps."""

from importlib import metadata

import click

from reflex_generate.generator import ModelGenerator
from reflex_generate.parser import ModelParser
from reflex_generate.utils import get_app_root


@click.group()
@click.version_option(metadata.version("reflex-generate"), message="%(version)s")
def cli():
    """Reflex-Generate CLI to create HTTP Resources for Reflex apps."""
    from reflex_generate.utils import check_dependencies

    check_dependencies()
    pass


@cli.command()
@click.argument("model_name", nargs=1)
@click.argument("fields", nargs=-1)
def scaffold(model_name: str, fields: tuple[str, ...]):
    """Subcommand for managing the scaffolding of resources."""
    pass


@cli.command()
@click.argument("model_name", nargs=1)
@click.argument("fields", nargs=-1)
def model(model_name: str, fields: tuple[str, ...]):
    """Subcommand for managing the creation of models."""
    parser = ModelParser(model_name, fields)
    generator = ModelGenerator(parser, get_app_root())
    generator.generate()


if __name__ == "__main__":
    cli()
