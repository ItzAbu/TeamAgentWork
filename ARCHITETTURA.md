# Architettura del Sistema - Gestionale di Magazzino (Flask + SQLite)

Questo documento definisce l'architettura tecnica del sistema, specificando lo schema del database SQLite e gli endpoint delle API RESTful esposte dal backend Flask.

---

## 1. Schema del Database SQLite (`schema.sql`)

Il database si compone di due tabelle principali: `prodotti` e `movimenti`.

### Tabella `prodotti`
Memorizza l'anagrafica degli articoli gestiti in magazzino.

| Colonna | Tipo | Vincoli / Descrizione |
| :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `sku` | TEXT | UNIQUE, NOT NULL - Codice univoco articolo |
| `nome` | TEXT | NOT NULL - Nome descrittivo del prodotto |
| `descrizione` | TEXT | Descrizione estesa opzionale |
| `prezzo` | REAL | NOT NULL, DEFAULT 0.0 - Prezzo unitario |
| `scorta_minima` | INTEGER | NOT NULL, DEFAULT 0 - Soglia minima per alert di sotto-scorta |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

### Tabella `movimenti`
Registra tutte le operazioni di carico (entrata) e scarico (uscita) merce.

| Colonna | Tipo | Vincoli / Descrizione |
| :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `prodotto_id` | INTEGER | FOREIGN KEY REFERENCES prodotti(id) ON DELETE CASCADE |
| `tipo` | TEXT | NOT NULL CHECK(tipo IN ('CARICO', 'SCARICO')) - Tipo operazione |
| `quantita` | INTEGER | NOT NULL CHECK(quantita > 0) - Quantità movimentata |
| `causale` | TEXT | Motivazione o nota opzionale (es. "Fornitura", "Vendita", "Reso") |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

## 2. API RESTful Backend (Flask)

Il backend espone un set di API JSON per la gestione del magazzino, consumate dal frontend tramite Fetch API.

### Anagrafica Prodotti

- **`GET /api/prodotti`**
  - **Descrizione**: Restituisce l'elenco di tutti i prodotti registrati.
  - **Risposta (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "sku": "ART-001",
        "nome": "Cacciavite Professionale",
        "descrizione": "Cacciavite a taglio 5x150mm",
        "prezzo": 12.50,
        "scorta_minima": 10,
        "created_at": "2025-02-18 10:00:00"
      }
    ]
    ```

- **`POST /api/prodotti`**
  - **Descrizione**: Inserisce un nuovo prodotto in anagrafica.
  - **Payload (JSON)**:
    ```json
    {
      "sku": "ART-002",
      "nome": "Martello da Carpentiere",
      "descrizione": "Manico in fibra di vetro",
      "prezzo": 18.00,
      "scorta_minima": 5
    }
    ```
  - **Risposta (201 Created)**: Oggetto prodotto creato con `id`.

- **`GET /api/prodotti/<id>`**
  - **Descrizione**: Dettaglio del singolo prodotto.

- **`DELETE /api/prodotti/<id>`**
  - **Descrizione**: Elimina un prodotto dall'anagrafica (ed eventuali movimenti associati tramite CASCADE).

---

### Gestione Movimenti (Carico / Scarico)

- **`POST /api/movimenti`**
  - **Descrizione**: Registra un'operazione di carico o scarico magazzino.
  - **Payload (JSON)**:
    ```json
    {
      "prodotto_id": 1,
      "tipo": "CARICO",
      "quantita": 50,
      "causale": "Rifornimento fornitore X"
    }
    ```
  - **Risposta (201 Created)**: Conferma della registrazione del movimento.

- **`GET /api/movimenti`**
  - **Descrizione**: Restituisce lo storico completo dei movimenti di magazzino (con JOIN sui prodotti).

---

### Giacenze e Dashboard (KPI)

- **`GET /api/giacenze`**
  - **Descrizione**: Calcola in tempo reale la giacenza attuale per ciascun prodotto (somma carichi - somma scarichi) e indica lo stato di sotto-scorta.
  - **Risposta (200 OK)**:
    ```json
    [
      {
        "prodotto_id": 1,
        "sku": "ART-001",
        "nome": "Cacciavite Professionale",
        "giacenza_attuale": 45,
        "scorta_minima": 10,
        "sotto_scorta": false
      }
    ]
    ```

- **`GET /api/dashboard`**
  - **Descrizione**: Restituisce indicatori di sintesi (KPI) per la dashboard iniziale.
  - **Risposta (200 OK)**:
    ```json
    {
      "totale_prodotti": 15,
      "articoli_sotto_scorta": 2,
      "movimenti_recenti_count": 42
    }
    ```
