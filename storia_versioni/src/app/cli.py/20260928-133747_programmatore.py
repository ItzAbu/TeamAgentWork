"""
Command‑line interface for the application using Click.
"""

import click
from app.core import greet, add


@click.group()
def cli():
    """Root command group."""
    pass


@cli.command()
@click.argument("name")
def hello(name: str):
    """
    Greet the provided NAME and print the result.
    """
    result = greet(name)
    click.echo(result)


@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def add_cmd(a: int, b: int):
    """
    Add two integers and print the result in the required format.
    """
    result = add(a, b)
    click.echo(f"Result: {result}")


if __name__ == "__main__":
    cli()
