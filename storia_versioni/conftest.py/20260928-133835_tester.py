import pytest
from click.testing import CliRunner

@pytest.fixture
def runner():
    """Provides a Click CLI runner for invoking commands in tests."""
    return CliRunner()
