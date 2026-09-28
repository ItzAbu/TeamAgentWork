# Segnalazione Bug - Magazzino API (`app.py`)

Durante l'analisi e la stesura dei test per l'applicazione Flask in `progetto/app.py`, sono stati identificati i seguenti bug e aree di miglioramento:

## 1. Gestione della chiusura della connessione DB in caso di eccezioni (`IntegrityError`)
- **Endpoint:** `POST /api/prodotti`
- **Descrizione:** Nel blocco `try...except sqlite3.IntegrityError:`, se si verifica un errore di integrità (es. SKU già esistente), viene eseguito `db.close()` all'interno dell'`except`, ma subito dopo viene eseguito anche il blocco `finally` che chiama nuovamente `db.close()`.
- **Impatto:** Sebbene in SQLite/Python chiamare `close()` più volte su una connessione non sempre sollevi eccezioni fatali a seconda del driver, rappresenta una pratica scorretta che può causare comportamenti indefiniti o errori a seconda della versione di sqlite3.

## 2. Mancanza di validazione sui campi numerici (`prezzo`, `scorta_minima`)
- **Endpoint:** `POST /api/prodotti`
- **Descrizione:** Vengono accettati valori negativi o non numerici (se non gestiti a livello di payload JSON) per `prezzo` e `scorta_minima`.
- **Impatto:** Un prezzo negativo o una scorta minima negativa non vengono validati esplicitamente, consentendo inserimenti anomali nel database.

## 3. Gestione della quantità nei movimenti con valori negativi o stringhe non convertibili
- **Endpoint:** `POST /api/movimenti`
- **Descrizione:** La validazione controlla `quantita > 0` tramite un blocco `try...except ValueError`. Tuttavia, se viene passato un float (es. `10.5`) o un booleano (`True`), `int(quantita)` converte il valore (es. `10.5` diventa `1`), oppure `quantita <= 0` potrebbe non intercettare input particolari.
- **Impatto:** Potrebbero essere accettate quantità decimali troncate silenziosamente o booleani come quantità.

## 4. Mancanza di test o gestione per eliminazione prodotti con movimenti associati (Foreign Key Constraints)
- **Endpoint:** `DELETE /api/prodotti/<int:id>`
- **Descrizione:** Lo schema definisce `FOREIGN KEY (prodotto_id) REFERENCES prodotti(id) ON DELETE CASCADE`, ma in SQLite i vincoli di Foreign Key (`PRAGMA foreign_keys = ON;`) **non sono abilitati di default** a meno che non vengano esplicitamente attivati su ogni connessione aperta (`conn.execute("PRAGMA foreign_keys = ON")`).
- **Impatto:** Eliminando un prodotto con movimenti associati, senza `PRAGMA foreign_keys = ON`, i movimenti orfani rimarrebbero nel database violando l'integrità referenziale.
