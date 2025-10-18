# Vulcano

Vulcano è un'applicazione per l'analisi di documenti PDF, composta da backend (BE), frontend (FE) e servizi di persistenza gestiti tramite Docker Compose.

## Backend

- **Tecnologie:** Python, Flask
- **Funzionalità principali:**
  - Gestione utenti: login, logout, cambio e recupero password
  - Interfaccia con AI generativa: invio file e domande, ricezione risposte con elenco dei file utilizzati
  - Endpoint per il download dei file
  - Sistema di cache delle risposte tramite Redis
  - Salvataggio e recupero dei file tramite database vettoriale (Qdrant)
- **Persistenza:**
  - Database PostgreSQL per la gestione utenti
  - Qdrant per la gestione dei file PDF
  - Protezione dei file tramite Row-Level Security

## Frontend

- **Tecnologie:** Typescript, React, Vite
- **Funzionalità principali:**
  - Gestione autenticazione utente: login, logout, cambio e recupero password
  - Caricamento e analisi dei file PDF
  - Visualizzazione dei risultati dell’analisi
  - Supervisione dei file caricati
  - Visualizzazione delle fonti interne delle risposte ottenute

## Avvio del progetto

Il progetto include una configurazione Docker Compose per avviare tutti i servizi necessari (backend, frontend, database).

## Note

Per maggiori dettagli sull’installazione e la configurazione, consultare la documentazione dei singoli componenti.