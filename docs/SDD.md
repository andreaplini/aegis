# System Design Description — SDD

> Bozza starter v0.2 — 15 novembre 2026
> Stato: architettura iniziale, da affinare dopo la scelta di fonti e area pilota.  
> Struttura derivata dal [template convertito in Markdown](template.md); file sorgente e risorse sono in `templates/` e `assets/`.

## 1. Introduzione

### 1.1 Scopo del sistema

Descrivere l’architettura software della piattaforma di mobilità urbana accessibile, tracciando i requisiti del [RAD](RAD.md) verso componenti, dati, API e operazioni.

### 1.2 Obiettivi di progettazione

- Mantenere indipendenti dominio, casi d’uso e adattatori.
- Mostrare provenienza e freschezza, trattando dati assenti/scaduti come sconosciuti.
- Integrare fonti e provider sostituibili tramite porte.
- Conservare uno storico append-only delle decisioni di moderazione.
- Supportare accessibilità, sicurezza, privacy e operatività misurabile.

### 1.3 Definizioni, acronimi e abbreviazioni

Vedere il glossario del [RAD](RAD.md#6-glossario). In questo documento: API = interfaccia HTTP applicativa; DTO = oggetto di trasporto; SRID = identificatore del riferimento spaziale.

### 1.4 Riferimenti

- [RAD — requisiti e analisi](RAD.md).
- [Template RAD/SDD convertito](template.md).
- Specifica OpenAPI: da generare e versionare con l’API.

### 1.5 Panoramica

La soluzione è composta da interfaccia web responsive renderizzata con Jakarta Faces e Facelets, API REST Jakarta EE, PostgreSQL/PostGIS, object storage e worker asincroni. La mappa usa una libreria cartografica nel browser e riceve i dati dall’API. Gli adattatori isolano routing, fonti di trasporto, notifiche e storage.

La versione di Jakarta EE e il runtime compatibile sono da selezionare in base ai requisiti di distribuzione e alle dipendenze effettive; non sono ancora decisioni convalidate.

## 2. Sistema corrente

Non è stato fornito un sistema software esistente: il progetto è greenfield. Integrazioni, dati legacy e procedure correnti dovranno essere rilevati durante l’analisi dell’area pilota.

## 3. Sistema proposto

### 3.1 Panoramica

```text
Browser (Facelets, HTML e JavaScript accessibile)
    │ HTTPS / HTML e JSON
    ▼
Runtime Jakarta EE
    ├── Jakarta Faces / Facelets
    ├── API REST versionata (Jakarta REST)
    ├── places / accessibility
    ├── routing
    ├── reports / moderation
    ├── identity
    └── integrations
          ├── PostgreSQL + PostGIS
          ├── Object storage compatibile S3
          ├── TransitDataProvider ── fonti ufficiali
          ├── RoutingProvider ───── provider percorsi
          ├── NotificationPort ──── canali notifiche
          └── Worker ────────────── sincronizzazioni e processi lenti
```

### 3.2 Decomposizione del sistema

| Sottosistema | Responsabilità |
|---|---|
| Frontend | Viste server-side Jakarta Faces/Facelets, ricerca, mappa/elenco accessibile, percorsi, dettagli, segnalazioni e interfaccia moderatore. |
| Places | Gestione e ricerca geospaziale di luoghi e fermate. |
| Accessibility | Gestione di feature, stati, fonti, timestamp e validità. |
| Routing | Validazione richieste, invocazione provider e presentazione dell’incertezza. |
| Reports | Creazione, tracking e gestione del ciclo di vita delle segnalazioni. |
| Moderation | Autorizzazione dei moderatori, transizioni e storico append-only. |
| Identity | Autenticazione, ruoli e separazione dei dati identificativi. |
| Integrations | Adattatori per fonti, routing, notifiche e object storage. |
| Worker | Sincronizzazioni schedulate, retry e attività asincrone idempotenti. |

Organizzazione Java proposta:

```text
com.example.mobility
├── places/{domain,application,adapter}
├── accessibility/{domain,application,adapter}
├── routing/{domain,application,adapter}
├── reports/{domain,application,adapter}
├── identity/{domain,application,adapter}
├── integrations
└── shared
```

Il dominio contiene entità, value object, invarianti e regole. L’application layer orchestra casi d’uso transazionali e definisce porte. Controller, repository e integrazioni sono adattatori sottili. DTO HTTP, modello di dominio e modello di persistenza restano separati.

### 3.3 Hardware/Software mapping

| Nodo/ambiente | Software e responsabilità |
|---|---|
| Browser/dispositivo utente | Frontend web responsive e tecnologie assistive. |
| Container applicativo | Runtime Jakarta EE con Jakarta Faces/Facelets per le viste e Jakarta REST per le API versionate. |
| Container worker | Sincronizzazioni e processi asincroni. |
| Database | PostgreSQL con estensione PostGIS e backup automatici gestiti. |
| Object storage | Foto e oggetti caricati, con accesso controllato e scadenza. |
| CDN/ingress | Distribuzione frontend, terminazione TLS e instradamento verso API secondo configurazione. |
| Servizi esterni | Fonti di trasporto, routing e notifiche tramite adattatori. |

In sviluppo usare Docker Compose con PostgreSQL/PostGIS e storage locale compatibile S3. In produzione gli specifici servizi gestiti restano da selezionare.

### 3.4 Gestione dei dati persistenti

#### Entità e tabelle previste

| Entità/tabella | Contenuto e vincoli principali |
|---|---|
| `place` | Nome, tipo, geometria con SRID esplicito; indici spaziali. |
| `accessibility_feature` | Tipo, stato, fonte, validità e timestamp; collegamento a `place`. |
| `transit_line`, `transit_stop` | Rete e fermate importate con riferimenti alla fonte. |
| `report` | Geometria/luogo, categoria, descrizione, stato e date; identità separata. |
| `report_event` | Eventi append-only con autore, data, decisione e riferimento duplicato. |
| `user_account` | Identità, credenziali/identity reference e ruoli con accesso limitato. |
| `source_sync` | Fonte, versione, timestamp, esito e controlli qualità. |

Applicare chiavi esterne, vincoli, indici di ricerca e spaziali. Usare migrazioni versionate e compatibili con le versioni applicative durante il rilascio progressivo. Le coordinate sono rappresentate con `GeoPoint`, value object immutabile con controlli di validità.

Ogni operazione di moderazione aggiorna lo stato corrente e inserisce un evento nella stessa transazione. Gli eventi non vengono modificati o eliminati dall’applicazione ordinaria.

#### Freschezza dei dati

La validità è definita per fonte e tipo di caratteristica. I dati oltre scadenza e quelli mancanti sono restituiti come sconosciuti. Il provider di routing non deve considerarli prove di compatibilità.

### 3.5 Controllo accessi e sicurezza

- Consultazione dei luoghi e dei percorsi pubblica secondo rate limit e policy applicabili.
- Invio segnalazioni e moderazione protetti dalle policy di identità e ruolo da definire.
- Autorizzazione verificata lato server per ogni operazione riservata.
- TLS per le comunicazioni; segreti gestiti fuori dal codice.
- Query parametrizzate, validazione server-side, rate limiting e risposte d’errore uniformi.
- Upload con limiti di dimensione/tipo, scansione, accesso controllato e scadenza.
- Log strutturati senza credenziali, tracking code o descrizioni personali; audit delle azioni amministrative.
- Tempi di conservazione, cancellazione e consenso immagini da definire prima del lancio.

### 3.6 Decisioni sul flusso di controllo globale

I controller validano la forma della richiesta e invocano un caso d’uso. Il caso d’uso applica le regole di dominio, coordina porte e transazioni e restituisce un risultato applicativo. Gli adattatori convertono tale risultato in DTO e risposte HTTP.

Porte applicative proposte:

```java
interface ReportRepository {
    Optional<Report> findById(ReportId id);
    Optional<Report> findByTrackingCode(TrackingCode code);
    Report save(Report report);
}

interface TransitDataProvider {
    SyncResult synchronize(SyncRequest request);
}

interface RoutingProvider {
    RouteOptions plan(RouteRequest request);
}

interface NotificationPort {
    void send(Notification notification);
}
```

#### API REST iniziali

| Metodo | Endpoint | Accesso/risultato |
|---|---|---|
| `GET` | `/api/v1/places?bbox=...` | Pubblico; luoghi per area. |
| `GET` | `/api/v1/places/{id}` | Pubblico; dettaglio luogo. |
| `GET` | `/api/v1/places/{id}/accessibility` | Pubblico; feature con fonte e freschezza. |
| `POST` | `/api/v1/routes` | Pubblico; percorsi e tratti non verificati. |
| `POST` | `/api/v1/reports` | Policy di invio da definire; crea report e tracking code. |
| `GET` | `/api/v1/reports/track/{code}` | Restituisce solo lo stato consentito al possessore del codice. |
| `GET` | `/api/v1/moderation/reports` | Ruolo moderatore; coda. |
| `POST` | `/api/v1/moderation/reports/{id}/events` | Ruolo moderatore; decisione con audit. |

OpenAPI documenta schemi, autenticazione, errori, paginazione e codici HTTP. Si usa una forma d’errore uniforme; la validazione è ripetuta a livello applicativo/domain dove protegge invarianti.

#### Precondizioni e postcondizioni applicative

| Operazione | Precondizioni | Postcondizioni |
|---|---|---|
| Ricerca luoghi/accessibilità | Parametri validi; ID o area nel formato previsto. | Risposta di sola lettura; fonti e freschezza presenti; assente/scaduto indicato sconosciuto. |
| Pianificazione percorso | Origine, destinazione e vincoli validi; input entro i limiti. | Alternative e stato di verifica restituiti; dato incerto non promosso ad accessibile; nessuna modifica persistente. |
| Creazione report | Campi validi; policy, rate limit e upload conformi. | Report ed evento iniziale persistiti atomicamente; tracking code restituito; niente dati parziali in errore. |
| Tracking report | Codice nel formato previsto. | Solo stato autorizzato restituito; nessuna modifica né divulgazione di dati riservati. |
| Moderazione report | Utente autorizzato; report esistente; transizione ammessa e motivazione presente. | Stato ed evento append-only persistiti nella stessa transazione; errore lascia entrambi invariati. |

### 3.7 Condizioni limite

- Provider di routing indisponibile: restituire errore comprensibile o fallback esplicitamente non verificato, senza inventare percorsi accessibili.
- Fonte assente, scaduta o incoerente: marcare l’informazione come sconosciuta e generare metriche/alert secondo soglie configurate.
- Nessun percorso compatibile: restituire esito esplicito e alternative non pienamente verificate, quando disponibili.
- Report inesistente o codice errato: risposta coerente che non consenta enumerazione dei report.
- Conflitto di moderazione o transizione non valida: rifiutare la modifica senza alterare stato o storico.
- Upload non valido o scansione fallita: rifiutare/quarantinare il file; non renderlo pubblico.
- Retry di sincronizzazione: usare operazioni idempotenti o chiavi di deduplicazione.
- Aggiornamento urgente: invalidare cache dell’area coinvolta e rendere osservabile l’esito.

## 4. Servizi del sottosistema

| Caso d’uso/servizio | Componenti principali | Transazione/effetti |
|---|---|---|
| Consultazione luoghi | Places API, `PlaceRepository`, PostGIS | Read-only; query spaziale. |
| Consultazione accessibilità | Accessibility API, repository feature e policy freschezza | Read-only; scadenza valutata prima della risposta. |
| Pianificazione | Routing API, `RoutingProvider`, dati accessibilità | Nessuna scrittura di dominio; output marcato con incertezza. |
| Creazione segnalazione | Reports API, `CreateReport`, `ReportRepository`, storage upload | Persistenza report+evento atomica; upload in quarantena/scansione. |
| Tracking | Tracking API, `ReportRepository` | Read-only; risposta minimizzata. |
| Moderazione | Moderation API, `ModerateReport`, repository | Stato ed evento in un’unica transazione. |
| Sincronizzazione | Worker, `TransitDataProvider`, `SourceSyncRepository` | Job schedulato, idempotente; audit esito/versione/timestamp. |
| Notifica | `NotificationPort` e adattatore del canale | Asincrona; retry e deduplicazione da definire. |

## 5. Glossario

| Termine | Definizione |
|---|---|
| Adattatore | Implementazione sostituibile di una porta verso HTTP, database o sistema esterno. |
| Dato sconosciuto | Dato assente o non valido/scaduto che non permette di determinare accessibilità. |
| Feature di accessibilità | Caratteristica dichiarata di un luogo, con stato e provenienza. |
| Porta | Interfaccia applicativa che descrive una dipendenza richiesta dal caso d’uso. |
| ReportEvent | Evento immutabile che registra una transizione o decisione sul report. |
| Tracking code | Codice non enumerabile per consultare lo stato della segnalazione. |
