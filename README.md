# Vulcano

> ⚠️ **Progetto incompleto:** Vulcano è un MVP in fase di sviluppo. Alcune funzionalità sono parziali o assenti e il codice non è pensato per l'uso in produzione. Le credenziali indicate in questo README sono fittizie e valgono solo per l'ambiente di sviluppo locale.

Vulcano è un'applicazione web per **interrogare i propri documenti PDF in linguaggio naturale**. Carichi i tuoi file, fai una domanda in chat e ricevi una risposta generata dall'AI basata sul contenuto dei documenti, insieme all'elenco dei file da cui l'informazione è stata presa.

## Panoramica

**A cosa serve**
- Trovare rapidamente informazioni all'interno di più documenti PDF senza doverli leggere tutti
- Ottenere risposte verificabili: ogni risposta indica i documenti sorgente, che si possono scaricare e consultare
- Tenere in un unico spazio personale (con login) i propri documenti e lo storico delle domande

**Come funziona** (Retrieval-Augmented Generation)
1. **Caricamento:** il PDF viene salvato su MinIO, il testo viene estratto e diviso in chunk
2. **Indicizzazione:** ogni chunk viene trasformato in embedding (OpenAI) e salvato in Qdrant
3. **Domanda:** la domanda dell'utente viene riformulata e usata per recuperare i chunk più rilevanti
4. **Risposta:** un LLM (OpenAI) genera la risposta a partire dai chunk recuperati; il risultato viene messo in cache su Redis

La pipeline AI è costruita con la libreria `datapizza-ai`.

**Architettura**
- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python + Flask, con API REST documentate tramite Swagger
- **Servizi:** PostgreSQL (utenti), MinIO (file), Qdrant (ricerca vettoriale), Redis (cache), Mailhog (email di sviluppo)
- Tutto avviabile con Docker Compose

Il progetto è composto da backend (BE), frontend (FE) e servizi di persistenza gestiti tramite Docker Compose.

## Endpoint:
- FE -> http://localhost:5173
- BE -> http://localhost:5000 - swagger http://localhost:5000/apidocs
- postgres -> host: localhost - port: 5432 - user: vulcanoroot - password: stromboli
- qdrant -> http://localhost:6333/dashboard - user e password non configurati
- redis -> host: localhost - port: 6379 - db: 0 - user e password non configurati
- minio -> host: localhost - port: 9000 - user: minioadmin - password: minioadmin

## Backend

- **Tecnologie:** Python, Flask
- **Funzionalità principali:**
  - Gestione utenti: login, logout, cambio e recupero password
  - Interfaccia con AI generativa: invio file e domande, ricezione risposte con elenco dei file utilizzati
  - Endpoint per il download dei file
  - Sistema di cache delle risposte tramite Redis
  - Salvataggio e recupero dei file tramite bucket S3 compatibili (MinIO)
  - Mapping dei chunk dei documenti per analisi semantiche tramite Qdrant e datapizza-ai
- **Persistenza:**
  - Database PostgreSQL per la gestione utenti
  - MinIO per la gestione e storage dei file PDF, con bucket creati automaticamente
  - Qdrant per la gestione e ricerca vettoriale dei chunk dei documenti
  - Console Mailhog per simulare SMPT

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

### Avvio rapido con Makefile

Assicurati di avere [Docker](https://www.docker.com/get-started/) installato sul tuo sistema e [Make](https://www.gnu.org/software/make/).

Comandi Makefile:

```sh
make up        # Avvia tutti i servizi in background
make down      # Ferma e rimuove i container
make logs      # Mostra i log dei servizi
make build     # Builda le immagini docker
make restart   # Riavvia i servizi
make clean     # Rimuove tutto (container, volumi, orfani)
```


### Avvio con Docker Compose

Assicurati di avere [Docker](https://www.docker.com/get-started/) installato sul tuo sistema.

Apri un terminale ed esegui:

```sh
docker compose --env-file .env.dev --profile dev up -d
```

Questo comando avvierà tutti i servizi necessari con profilo di dev.

### Avvio dei servizi applicativi

**Backend (BE):**
La versione di python utilizzata è la 3.13.9
Se si vuole far partire il progetto in locale e non su docker:
```sh
cd vulcano-be
pip install -r requirements.txt
python -m flask run
```
Il backend sarà disponibile sulla porta **5000**.

**Frontend (FE):**
Versioni utilizzate:
- Node: v22.20.0
- npm: v11.6.2

Il progetto utilizza `package-lock.json` per la gestione delle dipendenze, assicurando installazioni riproducibili.

Se si vuole far partire il progetto in locale e non su docker:
```sh
cd vulcano-fe
npm install
npm run dev
```
Il frontend sarà disponibile sulla porta **5173**.
