"""Test per il comando CLI in app.cli."""
import pytest
from click.testing import CliRunner

from app.cli import cli


def test_cli_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["Mondo"])
    assert result.exit_code == 0


def test_cli_output_contains_name():
    runner = CliRunner()
    result = runner.invoke(cli, ["Alice"])
    assert "Alice" in result.output


def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    # Senza argomenti dovrebbe fallire o mostrare help
    assert result.exit_code != 0 or "Usage" in result.output
