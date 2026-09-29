"""Test per il modulo core."""
import pytest
from app.core import greet


class TestGreet:
    def test_greet_basic(self):
        assert greet("World") == "Hello, World!"

    def test_greet_with_name(self):
        assert greet("Alice") == "Hello, Alice!"

    def test_greet_empty_string(self):
        assert greet("") == "Hello, !"

    def test_greet_with_spaces(self):
        assert greet("  Bob  ") == "Hello,   Bob  !"
