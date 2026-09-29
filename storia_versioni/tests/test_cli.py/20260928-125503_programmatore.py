import pytest
from click.testing import CliRunner

from app.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_greet_command(runner):
    result = runner.invoke(cli, ["greet", "Alice"])
    assert result.exit_code == 0
    assert "Alice" in result.output


def test_greet_command_output_format(runner):
    result = runner.invoke(cli, ["greet", "Bob"])
    assert result.exit_code == 0
    assert "Bob" in result.output


def test_greet_command_no_args(runner):
    result = runner.invoke(cli, ["greet"])
    assert result.exit_code != 0
