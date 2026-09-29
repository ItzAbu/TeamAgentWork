"""Test per la business logic in core.py."""

import pytest
from src.app.core import add, multiply, calculate


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -1) == -2

    def test_zero(self):
        assert add(0, 0) == 0

    def test_floats(self):
        assert add(0.1, 0.2) == pytest.approx(0.3)


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative(self):
        assert multiply(-2, 3) == -6


class TestCalculate:
    def test_addition(self):
        assert calculate("3 + 4") == 7

    def test_subtraction(self):
        assert calculate("10 - 3") == 7

    def test_multiplication(self):
        assert calculate("3 * 4") == 12

    def test_division(self):
        assert calculate("10 / 2") == 5

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            calculate("5 / 0")

    def test_invalid_expression(self):
        with pytest.raises(ValueError):
            calculate("3 +")

    def test_invalid_operator(self):
        with pytest.raises(ValueError):
            calculate("3 % 4")
