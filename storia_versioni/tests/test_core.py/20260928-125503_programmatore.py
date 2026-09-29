"""Test per il modulo core."""
import pytest

from app.core import greet


class TestGreet:
    """Test per la funzione greet."""

    def test_greet_nome_normale(self):
        """Greet con un nome normale restituisce il saluto atteso."""
        assert greet("Mario") == "Ciao, Mario!"

    def test_greet_stringa_vuota(self):
        """Greet con stringa vuota restituisce il saluto con nome vuoto."""
        assert greet("") == "Ciao, !"

    def test_greet_nome_con_spazi(self):
        """Greet con nome contenente spazi interni."""
        assert greet("Maria Rossi") == "Ciao, Maria Rossi!"
