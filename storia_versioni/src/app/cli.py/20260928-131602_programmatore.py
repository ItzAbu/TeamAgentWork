"""CLI commands using Click."""
import click

from app.core import add, multiply, greet


@click.group()
def cli():
    """App CLI - Calcolatrice e utility."""
    pass


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def somma(a, b):
    """Calcola la somma di due numeri."""
    result = add(a, b)
    click.echo(f"{a} + {b} = {result}")


@cli.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def prodotto(a, b):
    """Calcola il prodotto di due numeri."""
    result = multiply(a, b)
    click.echo(f"{a} * {b} = {result}")


@cli.command()
@click.argument("name")
def saluta(name):
    """Saluta una persona."""
    click.echo(greet(name))
