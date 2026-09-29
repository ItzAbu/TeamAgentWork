"""Test per il modulo CLI."""
from click.testing import CliRunner
from app.cli import cli


class TestCliGreet:
    def test_greet_command(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["greet", "World"])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_greet_command_with_name(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["greet", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

    def test_greet_no_args(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["greet"])
        assert result.exit_code != 0
