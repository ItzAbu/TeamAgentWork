<file>
from app.cli import add

def test_add():
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(add, ['5', '4'])
    assert result.exit_code == 0
    assert result.output == "Result: 9\n"
