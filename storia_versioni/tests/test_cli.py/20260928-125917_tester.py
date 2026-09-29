import pytest
from click.testing import CliRunner
from app.cli import cli


class TestCli:
    def test_add_command(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["add", "2", "3"])
        assert result.exit_code == 0
        assert "5" in result.output

    def test_multiply_command(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["multiply", "3", "4"])
        assert result.exit_code == 0
        assert "12" in result.output

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage" in result.output
