import pytest
from click.testing import CliRunner
from app.cli import hello, add_cmd

@pytest.fixture
def runner():
    return CliRunner()

def test_hello_command(runner):
    result = runner.invoke(hello, ["World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output

def test_add_command(runner):
    result = runner.invoke(add_cmd, ["3", "6"])
    assert result.exit_code == 0
    assert "Result: 9" in result.output
