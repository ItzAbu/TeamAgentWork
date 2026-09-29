import pytest
from app.core import add_numbers

def test_add_numbers_positive():
    assert add_numbers(2, 3) == 5

def test_add_numbers_negative():
    assert add_numbers(-1, -1) == -2

def test_add_numbers_mixed():
    assert add_numbers(-5, 10) == 5
