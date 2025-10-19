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

- Interfaccia frontend responsive ottimizzata per dispositivi mobili
- Caricamento multiplo di file tramite file ZIP o 7z
- Supporto al caricamento di file XLSX
- Importazione di PDF e documenti XLSX da URL Confluence
- Funzione di ricerca all’interno degli allegati
- Gestione di ambienti multipli, ciascuno con i propri file dedicati
- titolo alle domande richieste in chat