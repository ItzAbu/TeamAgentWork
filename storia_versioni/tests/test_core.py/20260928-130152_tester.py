"""Test per la business logic in app.core."""
import pytest

from app.core import greet


def test_greet_returns_string():
    result = greet("Mondo")
    assert isinstance(result, str)


def test_greet_contains_name():
    result = greet("Alice")
    assert "Alice" in result


def test_greet_empty_name():
    result = greet("")
    assert isinstance(result, str)
