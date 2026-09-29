"""Tests for core business logic."""
from app.core import add, multiply, greet


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -1) == -2

    def test_mixed(self):
        assert add(-1, 1) == 0

    def test_floats(self):
        assert add(0.1, 0.2) == 0.3


class TestMultiply:
    def test_positive(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative(self):
        assert multiply(-2, 3) == -6


class TestGreet:
    def test_returns_greeting(self):
        assert greet("Mondo") == "Ciao, Mondo!"

    def test_empty_name(self):
        assert greet("") == "Ciao, !"
