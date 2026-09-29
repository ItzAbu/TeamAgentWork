"""Pytest fixtures per il progetto StockFlow."""
import pytest
import os
import tempfile

from app import create_app
from database import init_db, get_db


@pytest.fixture
def app():
    """Crea un'app Flask con database di test in memoria."""
    app = create_app(testing=True)
    with app.app_context():
        init_db()
        yield app


@pytest.fixture
def client(app):
    """Client di test Flask."""
    return app.test_client()


@pytest.fixture
def admin_user(app):
    """Crea un utente admin di test."""
    from models import create_user
    with app.app_context():
        user = create_user("admin_test", "adminpass", "admin")
        yield user


@pytest.fixture
def regular_user(app):
    """Crea un utente normale di test."""
    from models import create_user
    with app.app_context():
        user = create_user("user_test", "userpass", "user")
        yield user


@pytest.fixture
def sample_product(app):
    """Crea un prodotto di test."""
    from models import create_product
    with app.app_context():
        product = create_product(
            name="Prodotto Test",
            sku="SKU001",
            category="Test",
            quantity=100,
            min_quantity=10,
            price=9.99
        )
        yield product
