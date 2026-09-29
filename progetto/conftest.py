"""Pytest fixtures per StockFlow."""
import pytest
import os
import tempfile

from database import init_db, get_db
from app import create_app


@pytest.fixture
def db_fd():
    """Crea un DB temporaneo per i test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["DATABASE"] = path
    init_db()
    yield path
    os.unlink(path)


@pytest.fixture
def app(db_fd):
    """Crea l'app Flask con il DB di test."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Test client Flask."""
    return app.test_client()


@pytest.fixture
def admin_user(app):
    """Crea un utente admin nel DB di test."""
    from models import create_user
    with app.app_context():
        uid = create_user("admin", "admin123", "admin")
    return uid


@pytest.fixture
def regular_user(app):
    """Crea un utente normale nel DB di test."""
    from models import create_user
    with app.app_context():
        uid = create_user("user1", "user123", "user")
    return uid


@pytest.fixture
def sample_product(app):
    """Crea un prodotto di esempio."""
    from models import create_product
    with app.app_context():
        pid = create_product(
            name="Widget", sku="WGT-001", category="Parts",
            quantity=100, min_quantity=10, price=9.99
        )
    return pid
