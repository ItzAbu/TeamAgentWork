import click
from app.core import add_numbers

@click.group()
def cli():
    """Main entry point for the CLI."""
    pass

@cli.command()
@click.argument("name", required=False, default="World")
def hello(name):
    """Greet the user."""
    click.echo(f"Hello, {name}!")

@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def add(a, b):
    """Add two numbers and display the result."""
    result = add_numbers(a, b)
    click.echo(f"Result: {result}")
