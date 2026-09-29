import click

from .core import greet


@click.group()
def cli():
    """App da terminale."""
    pass


@cli.command()
@click.argument("name")
def greet_cmd(name):
    """Saluta una persona."""
    click.echo(greet(name))


if __name__ == "__main__":
    cli()
