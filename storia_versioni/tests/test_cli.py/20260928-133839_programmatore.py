from click.testing import CliRunner
from app.cli import cli


def test_add_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "5", "4"])
    assert result.exit_code == 0
    assert "Result: 9" in result.output


def test_add_negative():
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "-3", "7"])
    assert result.exit_code == 0
    assert "Result: 4" in result.output


def test_add_zero():
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "0", "0"])
    assert result.exit_code == 0
    assert "Result: 0" in result.output
