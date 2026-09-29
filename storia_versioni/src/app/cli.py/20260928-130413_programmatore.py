"""Comando CLI basato su Click."""

import click

from src.app.core import calculate


@click.group()
def cli():
    """App da terminale per calcoli aritmetici."""
    pass


@cli.command()
@click.argument("expression")
def calc(expression):
    """Calcola un'espressione aritmetica.
    
    Esempio: calc "3 + 4"
    """
    try:
        result = calculate(expression)
        click.echo(f"Risultato: {result}")
    except (ValueError, ZeroDivisionError) as e:
        click.echo(f"Errore: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    cli()
