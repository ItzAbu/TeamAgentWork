import os
import tempfile
import pytest
from app import app, init_db, DATABASE

@pytest.fixture
def client():
    # Create a temporary database for testing
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    
    # Override DATABASE in app module if needed, or patch it
    import app as app_module
    original_db = app_module.DATABASE
    app_module.DATABASE = app.config["DATABASE"]
    
    init_db()
    
    with app.test_client() as client:
        yield client
        
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
    app_module.DATABASE = original_db


def test_index(client):
    response = client.get("/")
    # index() serves index.html from static folder; if not present or present, let's check status code
    # Usually 200 or 404 depending on whether static/index.html exists. Let's assert status in [200, 404]
    assert response.status_code in [200, 404]


def test_create_and_get_prodotti(client):
    # GET empty prodotti
    res = client.get("/api/prodotti")
    assert res.status_code == 200
    assert res.get_json() == []

    # POST new prodotto
    payload = {
        "sku": "SKU001",
        "nome": "Prodotto Test",
        "descrizione": "Descrizione test",
        "prezzo": 10.5,
        "scorta_minima": 5
    }
    res = client.post("/api/prodotti", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["sku"] == "SKU001"
    assert data["nome"] == "Prodotto Test"
    assert data["prezzo"] == 10.5
    prodotto_id = data["id"]

    # GET prodotto by id
    res = client.get(f"/api/prodotti/{prodotto_id}")
    assert res.status_code == 200
    assert res.get_json()["id"] == prodotto_id

    # GET prodotti list
    res = client.get("/api/prodotti")
    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_create_prodotto_validation(client):
    # Missing SKU and nome
    res = client.post("/api/prodotti", json={"descrizione": "test"})
    assert res.status_code == 400

    # Duplicate SKU test
    payload = {"sku": "DUP01", "nome": "Test 1"}
    res = client.post("/api/prodotti", json=payload)
    assert res.status_code == 201

    payload_dup = {"sku": "DUP01", "nome": "Test 2"}
    res = client.post("/api/prodotti", json=payload_dup)
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_delete_prodotto(client):
    # Delete non-existent
    res = client.delete("/api/prodotti/999")
    assert res.status_code == 404

    # Create and delete
    res = client.post("/api/prodotti", json={"sku": "DEL01", "nome": "To Delete"})
    prod_id = res.get_json()["id"]

    res = client.delete(f"/api/prodotti/{prod_id}")
    assert res.status_code == 200

    res = client.get(f"/api/prodotti/{prod_id}")
    assert res.status_code == 404


def test_movimenti_e_giacenze(client):
    # Create product
    res = client.post("/api/prodotti", json={"sku": "MOV01", "nome": "Mov Prod", "scorta_minima": 2})
    prod_id = res.get_json()["id"]

    # Invalid movimento type
    res = client.post("/api/movimenti", json={"prodotto_id": prod_id, "tipo": "INVALID", "quantita": 10})
    assert res.status_code == 400

    # Scarico with insufficient quantity (giacenza 0)
    res = client.post("/api/movimenti", json={"prodotto_id": prod_id, "tipo": "SCARICO", "quantita": 5})
    assert res.status_code == 400

    # Carico
    res = client.post("/api/movimenti", json={"prodotto_id": prod_id, "tipo": "CARICO", "quantita": 10, "causale": "Initial stock"})
    assert res.status_code == 201
    mov = res.get_json()
    assert mov["tipo"] == "CARICO"
    assert mov["quantita"] == 10

    # Get movimenti list
    res = client.get("/api/movimenti")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

    # Check giacenze
    res = client.get("/api/giacenze")
    assert res.status_code == 200
    giacenze = res.get_json()
    assert len(giacenze) == 1
    assert giacenze[0]["giacenza_attuale"] == 10
    assert giacenze[0]["sotto_scorta"] is False

    # Scarico valid quantity
    res = client.post("/api/movimenti", json={"prodotto_id": prod_id, "tipo": "SCARICO", "quantita": 9})
    assert res.status_code == 201

    # Check giacenze (10 - 9 = 1, scorta_minima = 2 -> sotto_scorta should be True)
    res = client.get("/api/giacenze")
    assert res.status_code == 200
    giacenze = res.get_json()
    assert giacenze[0]["giacenza_attuale"] == 1
    assert giacenze[0]["sotto_scorta"] is True


def test_dashboard(client):
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.get_json()
    assert "totale_prodotti" in data
    assert "articoli_sotto_scorta" in data
    assert "movimenti_recenti_count" in data
