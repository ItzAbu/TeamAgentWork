import pytest

# Conftest can stay empty if no fixtures are needed.
# Adding a simple fixture for demonstration (optional).
@pytest.fixture
def sample_data():
    return {"a": 1, "b": 2}
