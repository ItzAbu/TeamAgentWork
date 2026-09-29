import pytest
from app.core import greet, add

def test_greet():
    assert greet("World") == "Hello, World!"

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, -2, 3),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
