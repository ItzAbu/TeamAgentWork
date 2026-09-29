"""Configurazione applicativa per StockFlow."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurazione di base."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE: str = os.path.join(BASE_DIR, "stockflow.db")

class TestConfig(Config):
    """Configurazione per i test."""
    TESTING = True
    DATABASE = os.path.join(BASE_DIR, "test_stockflow.db")
