import click
from .core import add

@click.group()
def cli():
    """Simple CLI for the app."""
    pass

@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def add_cmd(a: int, b: int):
    """
    Add two numbers and print the result.
    """
    result = add(a, b)
    click.echo(f"Result: {result}")

if __name__ == "__main__":
    cli()
