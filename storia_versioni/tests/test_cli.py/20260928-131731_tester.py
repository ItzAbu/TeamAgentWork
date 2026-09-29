import pytest
from click.testing import CliRunner
from app.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_hello(runner):
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output

def test_hello_empty(runner):
    result = runner.invoke(cli, ["hello", "--name", ""])
    assert result.exit_code == 0
    assert "Hello, !" in result.output

def test_add(runner):
    # The add command should sum two integers and print the result
    result = runner.invoke(cli, ["add", "4", "5"])
    assert result.exit_code == 0
    # Expected output format defined in the CLI implementation
    assert "Result: 9" in result.output
