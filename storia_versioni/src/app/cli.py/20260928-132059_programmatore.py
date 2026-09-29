import click

from app.core import add


@click.group()
def cli():
    """Simple CLI application."""
    pass


@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def add_cmd(a, b):
    """Add two numbers and print the result."""
    result = add(a, b)
    click.echo(f"Result: {result}")


if __name__ == "__main__":
    cli()
