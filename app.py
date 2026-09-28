import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prodotti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                descrizione TEXT,
                prezzo REAL NOT NULL DEFAULT 0.0,
                scorta_minima INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS movimenti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prodotto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('CARICO', 'SCARICO')),
                quantita INTEGER NOT NULL CHECK(quantita > 0),
                causale TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prodotto_id) REFERENCES prodotti(id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/prodotti", methods=["GET"])
def get_prodotti():
    db = get_db()
    cursor = db.execute("SELECT * FROM prodotti ORDER BY id DESC")
    prodotti = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(prodotti), 200


@app.route("/api/prodotti", methods=["POST"])
def create_prodotto():
    data = request.get_json()
    if not data or not data.get("sku") or not data.get("nome"):
        return jsonify({"error": "SKU e Nome sono obbligatori"}), 400

    sku = data.get("sku")
    nome = data.get("nome")
    descrizione = data.get("descrizione", "")
    prezzo = data.get("prezzo", 0.0)
    scorta_minima = data.get("scorta_minima", 0)

    db = get_db()
    try:
        cursor = db.execute(
            """
            INSERT INTO prodotti (sku, nome, descrizione, prezzo, scorta_minima)
            VALUES (?, ?, ?, ?, ?)
        """,
            (sku, nome, descrizione, prezzo, scorta_minima),
        )
        db.commit()
        prodotto_id = cursor.lastrowid
        cursor = db.execute("SELECT * FROM prodotti WHERE id = ?", (prodotto_id,))
        nuovo_prodotto = dict(cursor.fetchone())
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"error": "SKU già esistente"}), 400
    finally:
        db.close()

    return jsonify(nuovo_prodotto), 201


@app.route("/api/prodotti/<int:id>", methods=["GET"])
def get_prodotto(id):
    db = get_db()
    cursor = db.execute("SELECT * FROM prodotti WHERE id = ?", (id,))
    row = cursor.fetchone()
    db.close()
    if not row:
        return jsonify({"error": "Prodotto non trovato"}), 404
    return jsonify(dict(row)), 200


@app.route("/api/prodotti/<int:id>", methods=["DELETE"])
def delete_prodotto(id):
    db = get_db()
    cursor = db.execute("SELECT * FROM prodotti WHERE id = ?", (id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({"error": "Prodotto non trovato"}), 404

    db.execute("DELETE FROM prodotti WHERE id = ?", (id,))
    db.commit()
    db.close()
    return jsonify({"message": "Prodotto eliminato con successo"}), 200


@app.route("/api/movimenti", methods=["GET"])
def get_movimenti():
    db = get_db()
    query = """
        SELECT m.id, m.prodotto_id, p.sku, p.nome as prodotto_nome, m.tipo, m.quantita, m.causale, m.created_at
        FROM movimenti m
        JOIN prodotti p ON m.prodotto_id = p.id
        ORDER BY m.id DESC
    """
    cursor = db.execute(query)
    movimenti = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(movimenti), 200


@app.route("/api/movimenti", methods=["POST"])
def create_movimento():
    data = request.get_json()
    if not data or not data.get("prodotto_id") or not data.get("tipo") or not data.get("quantita"):
        return jsonify({"error": "prodotto_id, tipo e quantita sono obbligatori"}), 400

    prodotto_id = data.get("prodotto_id")
    tipo = data.get("tipo")
    quantita = data.get("quantita")
    causale = data.get("causale", "")

    if tipo not in ("CARICO", "SCARICO"):
        return jsonify({"error": "Tipo movimento non valido (CARICO o SCARICO)"}), 400

    try:
        quantita = int(quantita)
        if quantita <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({"error": "La quantità deve essere un intero positivo"}), 400

    db = get_db()
    cursor = db.execute("SELECT * FROM prodotti WHERE id = ?", (prodotto_id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({"error": "Prodotto non trovato"}), 404

    # Controllo giacenza in caso di scarico
    if tipo == "SCARICO":
        giacenza_cursor = db.execute(
            """
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'CARICO' THEN quantita WHEN tipo = 'SCARICO' THEN -quantita ELSE 0 END), 0) as giacenza
            FROM movimenti
            WHERE prodotto_id = ?
        """,
            (prodotto_id,),
        )
        giacenza_attuale = giacenza_cursor.fetchone()["giacenza"]
        if quantita > giacenza_attuale:
            db.close()
            return jsonify({"error": "Quantità in scarico superiore alla giacenza attuale"}), 400

    cursor = db.execute(
        """
        INSERT INTO movimenti (prodotto_id, tipo, quantita, causale)
        VALUES (?, ?, ?, ?)
    """,
        (prodotto_id, tipo, quantita, causale),
    )
    db.commit()
    movimento_id = cursor.lastrowid
    cursor = db.execute(
        """
        SELECT m.id, m.prodotto_id, p.sku, p.nome as prodotto_nome, m.tipo, m.quantita, m.causale, m.created_at
        FROM movimenti m
        JOIN prodotti p ON m.prodotto_id = p.id
        WHERE m.id = ?
    """,
        (movimento_id,),
    )
    nuovo_movimento = dict(cursor.fetchone())
    db.close()

    return jsonify(nuovo_movimento), 201


@app.route("/api/giacenze", methods=["GET"])
def get_giacenze():
    db = get_db()
    query = """
        SELECT 
            p.id as prodotto_id,
            p.sku,
            p.nome,
            p.scorta_minima,
            COALESCE(SUM(CASE WHEN m.tipo = 'CARICO' THEN m.quantita WHEN m.tipo = 'SCARICO' THEN -m.quantita ELSE 0 END), 0) as giacenza_attuale
        FROM prodotti p
        LEFT JOIN movimenti m ON p.id = m.prodotto_id
        GROUP BY p.id, p.sku, p.nome, p.scorta_minima
        ORDER BY p.id DESC
    """
    cursor = db.execute(query)
    giacenze = []
    for row in cursor.fetchall():
        item = dict(row)
        item["sotto_scorta"] = item["giacenza_attuale"] < item["scorta_minima"]
        giacenze.append(item)
    db.close()
    return jsonify(giacenze), 200


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    db = get_db()
    
    totale_prodotti = db.execute("SELECT COUNT(*) FROM prodotti").fetchone()[0]
    movimenti_recenti_count = db.execute("SELECT COUNT(*) FROM movimenti").fetchone()[0]
    
    giacenze_query = """
        SELECT 
            p.id as prodotto_id,
            p.scorta_minima,
            COALESCE(SUM(CASE WHEN m.tipo = 'CARICO' THEN m.quantita WHEN m.tipo = 'SCARICO' THEN -m.quantita ELSE 0 END), 0) as giacenza_attuale
        FROM prodotti p
        LEFT JOIN movimenti m ON p.id = m.prodotto_id
        GROUP BY p.id, p.scorta_minima
    """
    cursor = db.execute(giacenze_query)
    articoli_sotto_scorta = 0
    for row in cursor.fetchall():
        if row["giacenza_attuale"] < row["scorta_minima"]:
            articoli_sotto_scorta += 1

    db.close()
    
    return jsonify({
        "totale_prodotti": totale_prodotti,
        "articoli_sotto_scorta": articoli_sotto_scorta,
        "movimenti_recenti_count": movimenti_recenti_count
    }), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
