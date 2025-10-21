# Vulcano

Vulcano è un'applicazione per l'analisi di documenti PDF, composta da backend (BE), frontend (FE) e servizi di persistenza gestiti tramite Docker Compose.

## Backend

- **Tecnologie:** Python, Flask
- **Funzionalità principali:**
  - Gestione utenti: login, logout, cambio e recupero password
  - Interfaccia con AI generativa: invio file e domande, ricezione risposte con elenco dei file utilizzati
  - Endpoint per il download dei file
  - Sistema di cache delle risposte tramite Redis
  - Salvataggio e recupero dei file tramite bucket S3 compatibili (MinIO)
  - Mapping dei chunk dei documenti per analisi semantiche tramite Qdrant
  - Salvataggio chunk dei file con riferimento utenti e risposta
- **Persistenza:**
  - Database PostgreSQL per la gestione utenti
  - MinIO per la gestione e storage dei file PDF, con bucket creati automaticamente
  - Qdrant per la gestione e ricerca vettoriale dei chunk dei documenti
  - Protezione dei file tramite Row-Level Security

## Frontend

- **Tecnologie:** Typescript, React, Vite
- **Funzionalità principali:**
  - Gestione autenticazione utente
  - Caricamento e analisi dei file PDF
  - Visualizzazione dei risultati dell’analisi
  - Supervisione dei file caricati
  - Visualizzazione delle fonti interne delle risposte ottenute

## Avvio del progetto

Il progetto include una configurazione Docker Compose per avviare tutti i servizi necessari (backend, frontend, database, MinIO, Qdrant).

### Avvio rapido con Docker Compose

Assicurati di avere [Docker](https://www.docker.com/get-started/) installato sul tuo sistema.

Apri un terminale, spostati nella cartella `vulcano-docker` ed esegui:

```sh
docker compose --env-file .env.dev --profile dev up -d
```

Questo comando avvierà tutti i servizi necessari con profilo di dev.

### Avvio dei servizi applicativi

**Backend (BE):**
```sh
cd vulcano-be
python -m flask run
```
Il backend sarà disponibile sulla porta **5000**.

**Frontend (FE):**
```sh
cd vulcano-fe
npm install
npm run dev
```
Il frontend sarà disponibile sulla porta **5173**.

### Utilizzo di MinIO e Qdrant

Per accedere all'interfaccia web di MinIO, apri il browser e vai su:  
[http://localhost:9001](http://localhost:9001)  
Login:  
- **Username:** minioadmin  
- **Password:** minioadmin

## Feature in sviluppo

- Migliorare il visualizzatore PDF: aggiungere la navigazione tra pagine e una migliore esperienza di lettura
- Generazione automatica di un titolo riassuntivo tramite AI per ogni domanda inviata nella chat
- Gestione di domande e risposte di grandi dimensioni: se il contenuto supera una certa soglia, viene salvato come file su MinIO e indicizzato su Qdrant per facilitarne la ricerca e il recupero
- Interfaccia frontend responsive ottimizzata per dispositivi mobili
- Caricamento multiplo di file tramite file ZIP o 7z
- Supporto al caricamento di file XLSX
- Importazione di PDF e documenti XLSX da URL Confluence
- Funzione di ricerca all’interno degli allegati
- Gestione di ambienti multipli, ciascuno con i propri file dedicati
- Modificare il viewer del pdf per visualizzarlo e navigare meglio


Problemi concorrenza:
Accesso a Redis: operazioni concorrenti di lettura/scrittura su chiavi condivise possono causare race condition o dati incoerenti.
Scrittura su MinIO: upload simultanei di file con lo stesso nome per lo stesso utente potrebbero sovrascrivere dati.
Database: inserimenti o aggiornamenti concorrenti (ad esempio su utenti, file, domande/risposte) possono portare a duplicati, inconsistenza o deadlock se non gestiti correttamente.
Qdrant: aggiornamenti simultanei ai payload dei punti (ad esempio aggiunta di answer_id) potrebbero causare perdita di dati se non gestiti in modo atomico.
Gestione dei token JWT: refresh e invalidazione concorrente dei token potrebbero causare problemi di sicurezza.