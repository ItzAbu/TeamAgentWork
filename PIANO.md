# Piano MVP - Gestionale di Magazzino (Flask + SQLite + HTML/JS)

Questo documento definisce il piano per lo sviluppo dell'MVP del gestionale di magazzino e la suddivisione dei compiti tra gli agenti del team.

---

## 1. Architettura dell'MVP

- **Backend**: Python con **Flask**
- **Database**: **SQLite** (gestito via script di inizializzazione e query SQL / ORM leggero)
- **Frontend**: **HTML5, CSS (Bootstrap 5) e JavaScript (Fetch API)** per un'interfaccia reattiva e pulita.

---

## 2. Elenco dei File da Creare

```text
progetto/
├── app.py                  # Entry point Flask, configurazione rotte principali
├── database.py             # Connessione DB SQLite, funzioni di utilità e init-db
├── schema.sql              # Definizione tabelle (prodotti, movimenti)
├── requirements.txt        # Dipendenze Python (Flask, ecc.)
├── static/
│   ├── css/
│   │   └── style.css       # Stili personalizzati aggiuntivi
│   └── js/
│       └── app.js          # Logica frontend (chiamate AJAX/Fetch, rendering dinamico)
└── templates/
    └── index.html          # Interfaccia SPA (Single Page Application) o multi-tab Bootstrap
```

---

## 3. Ruoli e Assegnazione dei Compiti agli Agenti

### Agente 1: Database & Backend Engineer
- **Compiti**:
  - Creare `schema.sql` con tabelle `prodotti` (id, sku, nome, descrizione, prezzo, scorta_minima) e `movimenti` (id, prodotto_id, tipo [carico/scarico], quantita, data).
  - Implementare `database.py` per la gestione della connessione SQLite e l'inizializzazione del DB.
  - Sviluppare `app.py` esponendo le API RESTful:
    - `GET /api/prodotti` / `POST /api/prodotti` (Anagrafica)
    - `POST /api/movimenti` (Carico/Scarico con aggiornamento giacenze)
    - `GET /api/giacenze` (Calcolo giacenze attuali)
    - `GET /api/dashboard` (Statistiche e KPI di sintesi)
  - Creare `requirements.txt`.

### Agente 2: Frontend Developer
- **Compiti**:
  - Realizzare `templates/index.html` utilizzando Bootstrap 5 per una UI pulita con sezioni/tab dedicate a: Dashboard, Anagrafica Prodotti, Carico/Scarico, Giacenze.
  - Scrivere `static/js/app.js` per gestire il caricamento dinamico dei dati tramite Fetch API, la sottomissione dei form di carico/scarico e la validazione lato client.
  - Aggiungere eventuali stili custom in `static/css/style.css`.

### Agente 3: Project Manager (Revisione e QA)
- **Compiti**:
  - Supervisionare l'intero sviluppo e verificare che i requisiti MVP siano soddisfatti.
  - Eseguire la revisione finale del codice prodotto dal team e validare l'integrazione tra Flask, SQLite e Frontend.
