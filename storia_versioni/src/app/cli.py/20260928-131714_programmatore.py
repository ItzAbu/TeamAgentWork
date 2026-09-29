<file>
import click

@click.command()
@click.argument('x', type=int)
@click.argument('y', type=int)
def add(x, y):
    """Add two numbers."""
    from .core import add as core_add
    result = core_add(x, y)
    click.echo(f"Result: {result}")

if __name__ == '__main__':
    add()
