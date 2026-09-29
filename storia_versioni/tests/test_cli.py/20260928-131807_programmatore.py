import pytest
from click.testing import CliRunner
from src.app.cli import cli

def test_cli_add():
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "4", "5"])
    assert result.exit_code == 0
    # The CLI should output the result prefixed with "Result: "
    assert "Result: 9" in result.output
