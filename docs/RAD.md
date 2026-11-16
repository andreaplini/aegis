# RAD

## Documento di Analisi dei Requisiti

| Dato | Valore |
|---|---|
| Progetto | aegis |
| Corso | Da compilare |
| Docenti | Da compilare |
| Candidati | Da compilare |
| Anno accademico | Da confermare |

Bozza aggiornata il 16 novembre 2026. I requisiti sono da convalidare con persone con disabilità, enti di trasporto e responsabili delle fonti dati. Il prodotto non è ancora implementato. Decisioni e prove mancanti sono tracciate nella [roadmap](MILESTONES.md).

## SOMMARIO

| Sezione | Contenuto |
|---|---|
| [Introduzione](#introduzione) | [Scopo del sistema](#11-scopo-del-sistema), [area di dominio](#12-area-di-dominio) |
| [Sistema corrente](#sistema-corrente) | Contesto esistente |
| [Sistema proposto](#sistema-proposto) | [Panoramica](#31-panoramica), [requisiti funzionali](#32-requisiti-funzionali), [requisiti non funzionali](#33-requisiti-non-funzionali), [vincoli](#34-vincoli), [modelli di sistema](#35-modelli-di-sistema) |
| [Utenti del sistema](#351-utenti-del-sistema) | Ruoli e contesti |
| [Scenari](#352-scenari) | Flussi rappresentativi |
| [Modelli dei casi d’uso](#353-modelli-dei-casi-duso) | Diagramma globale e schede con condizioni d’ingresso e d’uscita |
| [Modello degli oggetti](#354-modello-degli-oggetti) | Entity, boundary e control |
| [Diagramma delle classi](#355-diagramma-delle-classi) | Struttura statica concettuale |
| [Diagrammi di sequenza](#356-diagrammi-di-sequenza) | Flussi principali del sistema |
| [Interfaccia utente](#interfaccia-utente) | [Prototipo](#41-descrizione-del-prototipo-realizzato), [test di usabilità](#42-test-di-usabilità), [valutazione ISO](#43-valutazione-dellusabilità-secondo-iso-9241-110) |
| [Obiettivi del test](#421-obiettivi-del-test) | Scopo della valutazione |
| [Metodologia usata](#422-metodologia-usata) | Partecipanti, compiti e misure |
| [Sintesi delle misure](#423-sintesi-delle-misure) | Risultati raccolti |
| [Analisi dei risultati](#424-analisi-dei-risultati) | Problemi osservati ed evidenze |
| [Sintesi delle interviste](#425-sintesi-delle-interviste) | Risultati qualitativi |
| [Raccomandazioni finali](#426-raccomandazioni-finali) | Interventi prioritizzati |
| [Dettaglio punteggi](#431-dettaglio-punteggi-assegnati) | Valutazione secondo ISO 9241-110 |
| [Profilo di valutazione visiva](#432-profilo-di-valutazione-visiva) | Rappresentazione dei punteggi raccolti |
| [Glossario](#glossario) | Termini e acronimi |

## INTRODUZIONE

### 1.1 SCOPO DEL SISTEMA

La web app aiuta le persone con disabilità a pianificare spostamenti urbani, consultare l’accessibilità di stazioni, fermate e mezzi e segnalare barriere o guasti. Il sistema mostra la fonte e la data di aggiornamento delle caratteristiche. Un dato assente o scaduto è sconosciuto e non viene interpretato come prova di accessibilità.

Gli obiettivi sono trovare e confrontare percorsi, consultare le caratteristiche dei luoghi, inviare e tracciare segnalazioni e permettere ai moderatori di gestirle senza perdere la cronologia. Il successo sarà valutato con prove sul campo e sessioni con persone con disabilità. Area pilota, partecipanti, metriche e soglie sono da definire.

| Obiettivo | Criterio di verifica |
|---|---|
| Trovare e confrontare percorsi | Le alternative rendono visibili barriere note e tratti non verificati. |
| Consultare l’accessibilità | Ogni caratteristica mostra stato, fonte e freschezza disponibili. |
| Inviare e tracciare segnalazioni | L’invio restituisce un codice utilizzabile per consultare lo stato. |
| Moderare segnalazioni | Le decisioni sono gestibili senza perdere la cronologia. |
| Usare i flussi essenziali con tecnologie assistive | Le prove verificano tastiera e screen reader. |

### 1.2 AREA DI DOMINIO

Il dominio comprende pianificazione della mobilità urbana, dati geospaziali di trasporto pubblico, accessibilità di luoghi e infrastrutture e raccolta moderata di segnalazioni. Il pilota geografico, i servizi di trasporto coinvolti e le fonti disponibili devono ancora essere concordati.

## SISTEMA CORRENTE

Il progetto è greenfield. Non è stato fornito un sistema esistente da descrivere o migrare. Prima del pilota vanno censiti i servizi già usati da operatori e persone con disabilità, i dataset disponibili e i flussi correnti di segnalazione.

## SISTEMA PROPOSTO

### 3.1 PANORAMICA

La consultazione pubblica offre ricerca per area, dettagli di accessibilità e pianificazione di percorsi alternativi. Il sistema distingue caratteristiche verificate positive o negative da quelle sconosciute. Un dato scaduto è segnalato come tale e trattato come sconosciuto. Non dimostra accessibilità. Le segnalazioni seguono un ciclo moderato e mantengono uno storico append-only.

### 3.2 REQUISITI FUNZIONALI

| ID | Responsabile dell’azione | Azione richiesta | Priorità | Caso d’uso |
|---|---|---|---|---|
| FR-01 | Sistema | Mostrare luoghi e informazioni di accessibilità per l’area richiesta. | Must | UC-02 |
| FR-02 | Sistema | Mostrare caratteristiche quali ascensori, rampe, accessi e annunci con stato, fonte, aggiornamento e validità. | Must | UC-01, UC-02 |
| FR-03 | Sistema | Classificare come sconosciuti i dati assenti o scaduti, senza inferire accessibilità. | Must | UC-01, UC-02 |
| FR-04 | Utente e sistema | Acquisire origine, destinazione ed esigenze. Calcolare e restituire percorsi alternativi. | Must | UC-01 |
| FR-05 | Sistema | Distinguere nei percorsi barriere note, tratti compatibili e tratti non verificati. | Must | UC-01 |
| FR-06 | Utente e sistema | Consentire la selezione di un luogo e mostrare dettagli di accessibilità e provenienza. | Must | UC-02 |
| FR-07 | Segnalatore | Inserire luogo, categoria, descrizione e data. Allegare facoltativamente una foto. | Must | UC-03 |
| FR-08 | Sistema | Generare e restituire un codice di tracking per consultare lo stato della segnalazione. | Must | UC-03, UC-04 |
| FR-09 | Moderatore e sistema | Consentire conferma, rifiuto, risoluzione o unione di duplicati. Registrare ogni decisione. | Must | UC-05 |
| FR-10 | Adattatore dati | Importare dati ufficiali e registrare versione, esito e timestamp della sincronizzazione. | Should | UC-06 |
| FR-11 | Sistema | Invalidare la cache dell’area interessata quando riceve un aggiornamento urgente. | Should | UC-06 |
| FR-12 | Sistema | Inviare notifiche secondo preferenze, autorizzazioni e consensi configurati. | Could | UC-03, UC-05, UC-06 |
| FR-13 | Sistema | Autenticare gli utenti e verificare i ruoli per le operazioni riservate, mantenendo pubblica la consultazione. | Must | UC-03, UC-05, UC-06 |

### 3.3 REQUISITI NON FUNZIONALI

| ID | Qualità | Azione richiesta | Criterio di verifica |
|---|---|---|---|
| NFR-01 | Accessibilità | Consentire di completare i flussi essenziali da tastiera e con screen reader. | Verificare compiti approvati, navigazione, focus, etichette e annunci con tastiera e tecnologie assistive. |
| NFR-02 | Accessibilità | Fornire una vista testuale equivalente alle informazioni presentate sulla mappa. | Confrontare per le stesse richieste luoghi, percorsi e stati disponibili nella mappa e nella vista testuale. |
| NFR-03 | Accessibilità | Verificare contrasto e fruibilità con zoom. | Verificare i criteri dello standard e del livello di conformità da concordare. Finché OPEN-06 resta aperto il requisito non è valutabile. |
| NFR-04 | Privacy | Minimizzare i dati personali e separare identità e segnalazioni pubbliche. | Prima del lancio approvare finalità, accessi, conservazione e cancellazione. Verificare autorizzazioni, scadenza e cancellazione con prove sui dati. |
| NFR-05 | Sicurezza | Proteggere le comunicazioni con TLS e le funzioni riservate con ruoli. | Verificare TLS sugli endpoint esposti e rifiuto lato server delle operazioni riservate per ruoli non autorizzati. |
| NFR-06 | Sicurezza | Applicare rate limiting, validazione server-side e protezione da injection agli endpoint. | Provare input malformati e injection. Verificare il rifiuto senza effetti parziali e il comportamento del rate limiting rispetto alle soglie approvate. |
| NFR-07 | Sicurezza | Controllare gli upload per tipo, dimensione e contenuto prima dell’uso o pubblicazione. | Provare file ammessi, non validi e con scansione fallita. Verificare rifiuto o quarantena e accesso controllato ai file. |
| NFR-08 | Affidabilità dati | Esporre provenienza e freschezza e applicare scadenze per fonte e tipo di dato. | Verificare fonte, timestamp e validità. Testare dati assenti, scaduti e incoerenti e confermare che risultino sconosciuti. |
| NFR-09 | Operatività | Produrre log strutturati senza dati sensibili e metriche operative. | In ambiente concordato verificare log e metriche di disponibilità, latenza, sincronizzazioni e coda di moderazione. Controllare che log e allarmi non espongano dati sensibili. |
| NFR-10 | Continuità | Configurare allarmi e backup automatici e svolgere prove di ripristino. | Eseguire e registrare una prova di ripristino e verificare l’integrità dei dati. Approvare gli obiettivi di ripristino prima del lancio. |
| NFR-11 | Performance | Misurare e mantenere entro soglie concordate la latenza API e il caricamento delle viste principali. | Misurare p95 in staging con concorrenza e dataset approvati. Il requisito non è valutabile finché target e carico non sono concordati. |
| NFR-12 | Compatibilità | Versionare le API e applicare migrazioni compatibili con le versioni applicative in distribuzione. | Verificare in prova di rilascio che le versioni applicative attive durante la migrazione possano completare le operazioni previste. |
| NFR-13 | Usabilità | Rendere i flussi principali comprensibili e coerenti, con feedback sul completamento delle operazioni. | Svolgere sessioni con compiti e criteri approvati, registrare misure e problemi osservati e riportare gli esiti nel RAD. |
| NFR-14 | Scalabilità | Dimensionare API, database, worker e indici spaziali in base alla crescita di utenti, luoghi e richieste. | Eseguire prove di carico con dataset e profilo concordati. Confrontare i risultati con gli obiettivi approvati prima del pilota. |
| NFR-15 | Manutenibilità | Mantenere separati dominio, casi d’uso e adattatori e documentare le interfacce e le procedure operative. | Effettuare revisione architetturale e verificare build ripetibile, test e documentazione delle interfacce e procedure. |
| NFR-16 | Portabilità | Distribuire API e worker in container e mantenere la configurazione specifica dell’ambiente esterna al codice. | Avviare la stessa versione degli artefatti negli ambienti approvati e verificare le funzioni essenziali con test smoke e configurazioni distinte. |

### 3.4 VINCOLI

| Vincolo | Specifica e stato |
|---|---|
| Piattaforma applicativa | Usare Java LTS e Jakarta EE per API e worker. Usare Jakarta Faces e Facelets per le viste server-side. Versioni e runtime sono da convalidare. |
| Persistenza e file | Usare PostgreSQL con PostGIS, migrazioni versionate e storage compatibile S3 per le immagini. |
| Struttura software | Separare frontend, casi d’uso, dominio e adattatori. Documentare API versionate con OpenAPI. |
| Accesso | La consultazione è pubblica. Autenticazione e ruoli per invio e moderazione sono da definire. |
| Dati di accessibilità | Ogni proprietà registra provenienza e validità. Dato assente o scaduto è sconosciuto. |
| Dati personali e immagini | Applicare consenso, accesso controllato, conservazione limitata e cancellazione secondo policy da concordare. |

### 3.5 MODELLI DI SISTEMA

#### 3.5.1 UTENTI DEL SISTEMA

| Utente/ruolo | Obiettivi | Contesto |
|---|---|---|
| Viaggiatore | Consultare luoghi e pianificare un viaggio secondo le proprie esigenze. | Web responsive, anche con tecnologie assistive. |
| Segnalatore | Inviare una barriera o un guasto e seguirne lo stato. | Pubblico. Autenticazione e possibilità di invio anonimo da definire. |
| Moderatore | Valutare segnalazioni e gestire duplicati. | Area riservata, autenticazione e ruolo richiesti. |
| Gestore fonte | Mantenere configurazione e qualità delle sincronizzazioni. | Ruolo operativo da definire. |
| Amministratore tecnico | Gestire configurazione, sicurezza e operatività. | Accesso privilegiato e audit. |

#### 3.5.2 SCENARI

| Nome | Attori partecipanti | Flusso degli eventi |
|---|---|---|
| Viaggio con esigenze selezionate | Viaggiatore, sistema, provider di routing | Il viaggiatore inserisce origine, destinazione ed esigenze. Il sistema richiede alternative al provider. Il sistema mostra tempi, cambi, barriere note e tratti non verificati. |
| Verifica di una fermata | Viaggiatore, sistema | Il viaggiatore seleziona una fermata. Il sistema recupera le caratteristiche disponibili. Il sistema mostra stato, fonte e validità, indicando come sconosciuti i dati assenti o scaduti. |
| Guasto temporaneo | Segnalatore, sistema, servizio di storage e scansione | Il segnalatore inserisce luogo, categoria, descrizione e data. Facoltativamente allega una foto. Il sistema registra la segnalazione e restituisce il codice di tracking. |
| Moderazione di un duplicato | Moderatore, sistema | Il moderatore esamina una segnalazione e la collega al duplicato esistente. Il sistema registra la decisione e conserva la cronologia precedente. |
| Aggiornamento di una fonte | Gestore fonte, sistema, fonte dati autorizzata | Il gestore avvia o controlla una sincronizzazione. Il sistema acquisisce i dati dalla fonte, applica i controlli di qualità, pubblica solo una generazione valida e registra l’esito. |

#### 3.5.3 MODELLI DEI CASI D’USO

##### Diagramma globale

Il confine di sistema separa i casi d’uso di `aegis` dagli attori e dai servizi esterni.

```mermaid
flowchart TB
  accDescr: I sei casi d'uso aegis e le associazioni con persone, provider di routing, fonti e servizi esterni.
  subgraph ACTORS[Attori e servizi esterni]
    direction LR
    V[Viaggiatore]
    S[Segnalatore]
    M[Moderatore]
    G[Gestore fonte]
    R[Provider di routing]
    D[Fonte dati autorizzata]
    O[Servizio di storage e scansione]
  end
  subgraph SYSTEM[aegis]
    direction LR
    UC01((UC-01 Pianificare un viaggio))
    UC02((UC-02 Consultare un luogo))
    UC03((UC-03 Inviare una segnalazione))
    UC04((UC-04 Seguire una segnalazione))
    UC05((UC-05 Moderare una segnalazione))
    UC06((UC-06 Aggiornare una fonte))
  end
  V --- UC01
  R --- UC01
  V --- UC02
  S --- UC03
  O --- UC03
  S --- UC04
  M --- UC05
  G --- UC06
  D --- UC06
```

##### Specifiche dei casi d’uso

Ogni caso d’uso specifica attori, condizioni d’ingresso e d’uscita, requisiti qualitativi e flusso degli eventi.

| ID | Caso d’uso | Titolo | Attore principale | Descrizione |
|---|---|---|---|---|
| UC-01 | Pianificazione | Pianificare un viaggio | Viaggiatore | Inserisce origine, destinazione ed esigenze e consulta percorsi alternativi con stato di verifica. |
| UC-02 | Consultazione | Consultare un luogo | Viaggiatore | Seleziona una stazione, fermata o luogo e consulta accessibilità, fonte e freschezza. |
| UC-03 | Segnalazione | Inviare una segnalazione | Segnalatore | Comunica una barriera o un guasto, allega facoltativamente una foto, riceve un codice di tracking e un’eventuale notifica secondo consenso e policy. |
| UC-04 | Tracking | Seguire una segnalazione | Segnalatore | Presenta il codice di tracking e consulta lo stato consentito della segnalazione. |
| UC-05 | Moderazione | Moderare una segnalazione | Moderatore | Conferma, respinge, risolve o unisce un duplicato conservando lo storico e attivando le notifiche consentite. |
| UC-06 | Sincronizzazione | Aggiornare una fonte | Gestore fonte | Avvia o controlla l’importazione di dati e consulta l’esito dei controlli. |

###### UC-01: Pianificare viaggio

| Campo | Specifica |
|---|---|
| Attori partecipanti | Viaggiatore, sistema, provider di routing. |
| Condizioni d’ingresso | Origine, destinazione ed esigenze specificate e valide. La consultazione non richiede autenticazione. |
| Condizioni d’uscita | Restituiti zero o più percorsi con tempi, cambi e stato di verifica. Fonte e freschezza sono esposte quando disponibili. Dati assenti o scaduti non risultano accessibili. |
| Requisiti qualitativi | Il sistema distingue barriere note, tratti compatibili e tratti non verificati e presenta alternative disponibili. |
| Flusso degli eventi | Il viaggiatore inserisce origine, destinazione ed esigenze. Il sistema valida la richiesta e la inoltra al provider. Il provider restituisce le alternative. Il sistema aggiunge stato di verifica e provenienza disponibili e mostra risultati e incertezze. |

###### UC-02: Consultare luogo

| Campo | Specifica |
|---|---|
| Attori partecipanti | Viaggiatore, sistema. |
| Condizioni d’ingresso | Luogo identificabile tramite ID o selezione geografica. Parametri validi. |
| Condizioni d’uscita | Dettaglio e caratteristiche note sono mostrati con fonte e validità. Dati assenti o scaduti sono indicati come sconosciuti. Nessuna modifica ai dati. |
| Requisiti qualitativi | Le informazioni presentate sulla mappa sono disponibili anche in forma testuale e risultano utilizzabili da tastiera e tecnologie assistive. |
| Flusso degli eventi | Il viaggiatore seleziona o cerca un luogo. Il sistema recupera dettaglio e caratteristiche. Il sistema valuta la freschezza secondo la validità della fonte. Il sistema mostra caratteristiche, fonte, aggiornamento e stati sconosciuti. |

###### UC-03: Inviare segnalazione

| Campo | Specifica |
|---|---|
| Attori partecipanti | Segnalatore, sistema, servizio di storage e scansione. |
| Condizioni d’ingresso | Campi obbligatori validi. Autorizzazione, rate limit, consenso e requisiti dell’eventuale upload conformi alla policy definita. |
| Condizioni d’uscita | Segnalazione ed evento iniziale persistiti. Codice di tracking restituito. In caso di errore non rimane una segnalazione parziale. |
| Requisiti qualitativi | Il modulo è accessibile. I dati identificativi sono minimizzati e separati dalla segnalazione. La foto non è pubblicata prima dei controlli previsti. |
| Flusso degli eventi | Il segnalatore inserisce luogo, categoria, descrizione e data. Facoltativamente allega una foto. Il sistema valida i campi e controlla l’upload. Il sistema registra segnalazione ed evento iniziale. Restituisce il codice di tracking e invia eventuali notifiche solo secondo consenso e policy. |

###### UC-04: Seguire segnalazione

| Campo | Specifica |
|---|---|
| Attori partecipanti | Segnalatore, sistema. |
| Condizioni d’ingresso | Codice di tracking valido fornito dal richiedente. Modalità di accesso da definire secondo OPEN-04. |
| Condizioni d’uscita | È mostrato solo lo stato consentito dalla policy di accesso approvata. Identità e dettagli riservati non sono esposti. Nessuna modifica al report. |
| Requisiti qualitativi | La risposta non consente l’enumerazione delle segnalazioni e comunica lo stato in forma accessibile. |
| Flusso degli eventi | Il segnalatore inserisce il codice. Il sistema lo verifica e recupera lo stato consentito. Il sistema mostra lo stato senza esporre dati riservati. |

###### UC-05: Moderare segnalazione

| Campo | Specifica |
|---|---|
| Attori partecipanti | Moderatore, sistema. |
| Condizioni d’ingresso | Moderatore autenticato e autorizzato. Report esistente. Transizione ammessa. Motivazione presente quando richiesta. |
| Condizioni d’uscita | Stato ed evento append-only aggiornati nella stessa transazione, con attore e timestamp. Una transizione non valida non modifica i dati. |
| Requisiti qualitativi | Ogni decisione è tracciabile. Gli eventi precedenti restano consultabili e non sono sovrascritti. |
| Flusso degli eventi | Il moderatore apre il report. Il sistema mostra i dati e la cronologia autorizzati. Il moderatore sceglie conferma, rifiuto, risoluzione o unione e inserisce la motivazione richiesta. Il sistema valida la transizione e registra stato ed evento nella stessa transazione. Invia eventuali notifiche solo secondo consenso e policy. |

###### UC-06: Aggiornare una fonte

| Campo | Specifica |
|---|---|
| Attori partecipanti | Gestore fonte, sistema e fonte dati autorizzata. |
| Condizioni d’ingresso | Fonte configurata e abilitata. Gestore autenticato e autorizzato quando l’avvio è manuale. Esecuzione schedulata ammessa dalla configurazione. |
| Condizioni d’uscita | Versione, timestamp, controlli ed esito della sincronizzazione registrati. Solo un insieme completo e validato diventa visibile. Un aggiornamento urgente invalida la cache dell’area interessata dopo la pubblicazione. Un errore mantiene disponibili i dati validi precedenti e non pubblica dati parziali. |
| Requisiti qualitativi | Retry idempotenti. Provenienza e freschezza conservate. Dati assenti, incoerenti o scaduti non sono presentati come accessibili. |
| Flusso degli eventi | Il gestore avvia o consulta il processo, oppure scatta la pianificazione. Il sistema invoca l’adattatore. L’adattatore acquisisce i dati in un insieme candidato non visibile agli utenti. Il sistema valida contratto, chiavi e qualità, quindi registra versione, timestamp, controlli ed esito. Se i controlli passano, pubblica l’insieme candidato con un passaggio atomico e invalida la cache interessata dopo la pubblicazione. Se l’acquisizione o la validazione falliscono, mantiene attivi i dati precedenti e registra l’esito senza pubblicare dati parziali. |

#### 3.5.4 MODELLO DEGLI OGGETTI

##### Oggetti entity dei casi d’uso

| Oggetto | Responsabilità |
|---|---|
| `Place` | Rappresenta luogo, fermata o stazione con identificativo, nome, tipo e geometria. |
| `AccessibilityFeature` | Rappresenta una caratteristica con stato esplicito, fonte, timestamp e validità, associata a un luogo. |
| `Report` | Rappresenta luogo/geometria, categoria, descrizione, stato, date e riferimento protetto per tracking. |
| `ReportEvent` | Registra in modo append-only attore, timestamp, decisione e riferimento a un eventuale duplicato. |
| `SourceSync` | Registra fonte, versione, esito, timestamp e controlli di qualità. |
| `UserAccount` | Rappresenta identità e ruoli. I dati identificativi sono separati dai contenuti pubblici. |
| `DataSource` | Rappresenta una fonte con identificativo, responsabile, versione e regola di validità da definire. |
| `TransitLine` e `TransitStop` | Rappresentano linee e fermate importate, con geometria e riferimenti alla fonte. |
| `GeoPoint` | Value object immutabile che rappresenta coordinate valide con riferimento spaziale esplicito. |

##### Oggetti boundary dei casi d’uso

| Oggetto | Responsabilità |
|---|---|
| API luoghi/accessibilità | Riceve richieste di ricerca e dettaglio e restituisce dati con fonte e freschezza. |
| API percorsi | Riceve origine, destinazione e vincoli e restituisce alternative con incertezza esplicita. |
| API segnalazioni e tracking | Riceve segnalazioni e richieste di tracking. Restituisce conferma o stato consentito. |
| API moderazione | Espone coda e operazioni di moderazione protette da autorizzazione. |
| Interfaccia web | Presenta mappa, viste testuali, percorsi, moduli e pannello di moderazione. |
| Gateway upload | Valida e inoltra le immagini al flusso controllato di storage e scansione. |

##### Oggetti control dei casi d’uso

| Oggetto | Responsabilità |
|---|---|
| `PlanRoute` | Coordina validazione della richiesta, provider e classificazione dell’incertezza. |
| `GetPlaceAccessibility` | Recupera le caratteristiche e applica le regole di freschezza. |
| `CreateReport` | Applica le regole di creazione e persiste report ed evento iniziale. |
| `TrackReport` | Recupera e limita le informazioni restituite tramite codice di tracking. |
| `ModerateReport` | Valida transizioni e persiste stato ed evento append-only in modo atomico. |
| `SynchronizeSource` | Coordina importazione, controlli di qualità e registrazione dell’esito. |

#### 3.5.5 DIAGRAMMA DELLE CLASSI

Il diagramma riassume le associazioni concettuali tra luoghi, caratteristiche di accessibilità, segnalazioni, eventi, coordinate e fonti.

```mermaid
classDiagram
  accDescr: Relazioni concettuali tra luoghi, caratteristiche, segnalazioni, eventi e fonti.
  class Place {
    PlaceId id
    String name
    PlaceType type
    GeoPoint position
  }
  class AccessibilityFeature {
    FeatureType type
    FeatureState state
    Instant observedAt
    Instant validUntil
  }
  class Report {
    ReportId id
    ReportCategory category
    ReportStatus status
    Instant createdAt
  }
  class ReportEvent {
    ReportEventId id
    ModerationDecision decision
    Instant occurredAt
  }
  class DataSource {
    SourceId id
    String name
    String version
  }
  class SourceSync {
    SyncResult result
    Instant completedAt
  }
  class TransitLine {
    TransitLineId id
    String name
  }
  class TransitStop {
    TransitStopId id
    GeoPoint position
  }
  class GeoPoint {
    Decimal latitude
    Decimal longitude
    Integer srid
  }
  Place --> AccessibilityFeature
  Place --> TransitStop
  TransitLine --> TransitStop
  Report --> ReportEvent
  Report --> GeoPoint
  Place --> GeoPoint
  AccessibilityFeature --> DataSource
  SourceSync --> DataSource
```

#### 3.5.6 DIAGRAMMI DI SEQUENZA

I diagrammi descrivono gli scambi tra attori, boundary, casi d’uso e porte esterne per i flussi principali.

##### Pianificazione di un viaggio

Il diagramma descrive la richiesta di alternative, l’integrazione del provider e la presentazione dell’incertezza.

```mermaid
sequenceDiagram
  accDescr: Il viaggiatore invia la richiesta e riceve percorsi con l'incertezza evidenziata.
  actor V as Viaggiatore
  participant UI as Interfaccia web
  participant API as API percorsi
  participant UC as PlanRoute
  participant RP as RoutingProvider
  V->>UI: Inserisce origine, destinazione ed esigenze
  UI->>API: Richiesta di percorso
  API->>UC: Richiesta validata
  UC->>RP: Calcola alternative
  RP-->>UC: Alternative e tratti
  UC-->>API: Percorsi con stato di verifica
  API-->>UI: Risultati
  UI-->>V: Percorsi e incertezze
```

##### Consultazione di un luogo

Il diagramma descrive il recupero dei dati di accessibilità e la valutazione della loro freschezza.

```mermaid
sequenceDiagram
  accDescr: Il sistema recupera luogo e caratteristiche, poi restituisce stato, fonte e validità.
  actor V as Viaggiatore
  participant UI as Interfaccia web
  participant API as API luoghi
  participant UC as GetPlaceAccessibility
  participant Repo as PlaceRepository
  V->>UI: Seleziona un luogo
  UI->>API: Richiede il dettaglio
  API->>UC: Identificativo validato
  UC->>Repo: Recupera luogo e caratteristiche
  Repo-->>UC: Dati e provenienza
  UC-->>API: Dettaglio con freschezza valutata
  API-->>UI: Risposta
  UI-->>V: Caratteristiche, fonte e stato
```

##### Invio di una segnalazione

Il diagramma mostra lo scambio tra segnalatore, API, caso d’uso e repository durante la creazione atomica di una segnalazione.

```mermaid
sequenceDiagram
  accDescr: L'API valida i dati e crea segnalazione ed evento in modo atomico.
  actor S as Segnalatore
  participant API as Reports API
  participant UC as CreateReport
  participant Repo as ReportRepository
  S->>API: POST segnalazione
  API->>UC: input validato
  UC->>Repo: salva Report + ReportEvent
  Repo-->>UC: report persistito
  UC-->>API: tracking code e stato
  API-->>S: conferma invio
```

Le transizioni ammesse di moderazione e gli stati completi del report sono da definire nel modello di dominio.

##### Tracking di una segnalazione

Il diagramma descrive la consultazione dello stato tramite codice senza esporre dati riservati.

```mermaid
sequenceDiagram
  accDescr: Il codice di tracking consente la consultazione dello stato autorizzato.
  actor S as Segnalatore
  participant UI as Interfaccia web
  participant API as API tracking
  participant UC as TrackReport
  participant Repo as ReportRepository
  S->>UI: Inserisce il codice di tracking
  UI->>API: Richiede lo stato
  API->>UC: Codice validato
  UC->>Repo: Recupera report
  Repo-->>UC: Stato e dati autorizzati
  UC-->>API: Stato minimizzato
  API-->>UI: Risposta
  UI-->>S: Stato consentito
```

##### Moderazione di una segnalazione

Il diagramma descrive la verifica della transizione e la registrazione atomica dello stato e dell’evento.

```mermaid
sequenceDiagram
  accDescr: La moderazione valida la transizione e registra stato ed evento nella stessa operazione.
  actor M as Moderatore
  participant UI as Pannello moderazione
  participant API as API moderazione
  participant UC as ModerateReport
  participant Repo as ReportRepository
  M->>UI: Seleziona decisione e motivazione
  UI->>API: Invia decisione
  API->>UC: Comando autorizzato
  UC->>Repo: Carica report e cronologia
  Repo-->>UC: Stato corrente
  UC->>UC: Verifica transizione
  UC->>Repo: Salva stato ed evento
  Repo-->>UC: Operazione completata
  UC-->>API: Esito
  API-->>UI: Conferma o errore
```

##### Sincronizzazione di una fonte

I diagrammi separano acquisizione e pubblicazione dalla lettura e pulizia cache. La query usa solo la generazione attiva letta dal repository autorevole. Il lavoro di pulizia è registrato con la pubblicazione e un fallimento non rende selezionabili le chiavi della generazione precedente.

```mermaid
sequenceDiagram
  accDescr: Il worker importa i dati in isolamento, valida la generazione candidata e registra pubblicazione ed effetto cache pendente nella stessa transazione. Un errore mantiene la generazione attiva precedente.
  actor G as Gestore fonte
  participant W as Worker
  participant P as TransitDataProvider
  participant R as Repository
  G->>W: Avvia o consulta sincronizzazione
  W->>P: Richiede aggiornamento
  P-->>W: Dati e versione
  W->>R: Scrive generazione candidata isolata
  W->>W: Valida schema, chiavi e qualità
  alt Validazione superata
    W->>R: Transazione: attiva generazione, registra esito e pulizia pendente
  else Acquisizione o validazione fallita
    W->>R: Registra errore e conserva la generazione attiva
  end
  W-->>G: Esito operativo
```

```mermaid
sequenceDiagram
  accDescr: La query legge dal repository la generazione attiva e usa una chiave cache versionata. Il worker recupera la pulizia pendente e può ripeterla dopo un errore.
  participant Q as Query luoghi
  participant R as Repository
  participant C as Cache geografica
  participant W as Worker pulizia cache
  Q->>R: Legge gli ID delle generazioni attive
  R-->>Q: Fonte e generazione attiva
  Q->>C: Cerca chiave per fonte, generazione e area
  alt Cache valida
    C-->>Q: Dati della generazione attiva
  else Cache assente
    Q->>R: Legge i dati della generazione attiva
    R-->>Q: Dati e provenienza
    Q->>C: Memorizza con la chiave versionata
  end
  loop Finché la pulizia è pendente
    W->>R: Recupera la pulizia pendente
    R-->>W: Fonte e generazione superata
    W->>C: Elimina le chiavi della generazione superata
    alt Pulizia completata
      W->>R: Registra il completamento
    else Cache non disponibile
      W->>R: Registra errore e mantiene il lavoro pendente
    end
  end
```

## INTERFACCIA UTENTE

Le viste iniziali sono: ricerca e preferenze di viaggio. Risultati e alternative. Mappa affiancata da elenco. Dettaglio luogo. Form segnalazione. Pagina tracking. Coda e dettaglio moderazione. Ogni informazione cartografica deve avere alternativa testuale e le interazioni devono supportare tastiera e screen reader. Wireframe e prototipo sono da realizzare e validare.

### 4.1 DESCRIZIONE DEL PROTOTIPO REALIZZATO

**Stato:** non ancora realizzato. Da documentare al completamento.

| Aspetto | Da specificare |
|---|---|
| Scopo/ruolo/interfaccia/implementazione | Da definire |
| Modo d’uso | Statico, dinamico o interattivo: da definire |
| Fedeltà | Bassa o alta: da definire |
| Completezza funzionale | Orizzontale o verticale: da definire |
| Durata | Usa e getta o evolutivo: da definire |

### 4.2 TEST DI USABILITÀ

**Stato:** pianificato, non eseguito.

#### 4.2.1 OBIETTIVI DEL TEST

Valutare se le persone riescono a pianificare un viaggio, interpretare freschezza e incertezza, consultare un luogo, inviare e seguire una segnalazione e completare i flussi con tastiera e screen reader. Obiettivi e criteri specifici sono da convalidare con i partecipanti.

#### 4.2.2 METODOLOGIA USATA

Il test non è ancora stato condotto. Numero, esperienza e caratteristiche dei partecipanti, compiti, scenari, ambiente, strumenti, modalità e durata delle sessioni per partecipante e nel complesso sono da definire con persone con disabilità. Prima delle sessioni vanno concordati consenso, misure raccolte, ruolo degli osservatori e metodo di analisi.

| Elemento metodologico | Definizione |
|---|---|
| Partecipanti ed esperienza | Da definire con persone con disabilità e in base ai profili d’uso del pilota. |
| Compiti e scenari | Pianificare un viaggio, consultare un luogo, inviare e seguire una segnalazione e usare i flussi con tecnologie assistive. Da convalidare prima delle sessioni. |
| Contesto e strumenti | Da definire. Registrare dispositivo, browser, tecnologie assistive e condizioni di rete usati. |
| Modalità e durata | Sessioni individuali o altra modalità da definire. Durata per partecipante e complessiva da registrare. |
| Misure | Tempi, completamento, errori, richieste di aiuto, comprensione di freschezza e incertezza e riscontri qualitativi. |
| Osservatori e analisi | Ruoli, metodo di registrazione, trattamento delle evidenze e metodo di analisi da definire prima dei test. |

#### 4.2.3 SINTESI DELLE MISURE

Risultati non disponibili perché il test non è stato eseguito. Le misure saranno raccolte per partecipante e compito, quindi aggregate per compito con unità e denominatori espliciti.

| Partecipante pseudonimizzato | Compito | Tempo di esecuzione | Completamento | Errori e note |
|---|---|---|---|---|
| Da raccogliere | Pianificare un viaggio | Da misurare | Da misurare | Da raccogliere |
| Da raccogliere | Consultare un luogo | Da misurare | Da misurare | Da raccogliere |
| Da raccogliere | Inviare e seguire una segnalazione | Da misurare | Da misurare | Da raccogliere |
| Da raccogliere | Completare i flussi con tecnologie assistive | Da misurare | Da misurare | Da raccogliere |

| Compito | Tempo medio o statistica concordata | Successo o misura aggregata | Errori e note aggregate |
|---|---|---|---|
| Pianificare un viaggio | Da calcolare | Da calcolare | Da raccogliere |
| Consultare un luogo | Da calcolare | Da calcolare | Da raccogliere |
| Inviare e seguire una segnalazione | Da calcolare | Da calcolare | Da raccogliere |
| Completare i flussi con tecnologie assistive | Da calcolare | Da calcolare | Da raccogliere |

Unità, soglie e modalità di aggregazione sono da concordare prima del test.

#### 4.2.4 ANALISI DEI RISULTATI

Analisi non disponibile perché il test non è stato eseguito. La tabella seguente raccoglie i campi da compilare per ogni partecipante e compito.

| Partecipante e compito | Problema osservato | Evidenza o screenshot | Gravità | Reazione o commento | Intervento necessario |
|---|---|---|---|---|---|
| Da rilevare durante il test | Da rilevare | Da raccogliere nel rispetto del consenso | Scala da definire | Da raccogliere | Da determinare dall’analisi |

#### 4.2.5 SINTESI DELLE INTERVISTE

Le interviste successive al test non sono state svolte. Le evidenze saranno sintetizzate dopo la raccolta, distinguendo osservazioni e interpretazioni.

#### 4.2.6 RACCOMANDAZIONI FINALI

Raccomandazioni non disponibili prima delle prove. Saranno ordinate per priorità e collegate ai problemi osservati.

| Problema collegato | Intervento migliorativo | Priorità | Stato |
|---|---|---|---|
| Da determinare dopo l’analisi | Da definire sulla base delle evidenze | Da assegnare | Non valutato |

### 4.3 VALUTAZIONE DELL’USABILITÀ SECONDO ISO 9241-110

La valutazione potrà essere condotta sul prototipo usando come riferimento [ISO 9241-110:2020](https://www.iso.org/standard/75258.html), indicata da ISO come edizione corrente e confermata nel 2025. L’adozione dello standard, il protocollo, i partecipanti, i risultati e i limiti restano da concordare secondo OPEN-06. Non sono stati assegnati punteggi.

#### 4.3.1 DETTAGLIO PUNTEGGI ASSEGNATI

La matrice riporta i sette principi dell’edizione 2020 per pianificare la valutazione. Scala, criteri ed evidenze saranno definiti nel protocollo approvato prima delle prove. I punteggi non sono stati assegnati perché il prototipo e le prove non sono disponibili.

| Principio valutato | Punteggio | Evidenza e motivazione |
|---|---|---|
| Idoneità ai compiti dell’utente | Non assegnato | Da valutare sul supporto ai compiti e agli obiettivi degli utenti. |
| Auto-descrittività | Non assegnato | Da valutare sulla comprensione di etichette, stati e controlli. |
| Conformità alle aspettative dell’utente | Non assegnato | Da valutare su coerenza di comportamenti, termini e presentazione. |
| Apprendibilità | Non assegnato | Da valutare sulla facilità di apprendimento e di ripresa dopo un’interruzione. |
| Controllabilità | Non assegnato | Da valutare su navigazione, possibilità di rivedere le scelte e controllo dell’interazione. |
| Robustezza agli errori d’uso | Non assegnato | Da valutare sulla prevenzione, segnalazione e correzione degli errori. |
| Coinvolgimento dell’utente | Non assegnato | Da valutare sull’interazione e sulla motivazione rispetto ai compiti d’uso. |

#### 4.3.2 PROFILO DI VALUTAZIONE VISIVA

Il profilo visivo non è disponibile perché i punteggi non sono stati raccolti. Dopo la valutazione potrà essere rappresentato con un diagramma radar dei sette principi. Una tabella accessibile e una descrizione testuale accompagneranno il grafico. Non saranno introdotti valori non osservati.

## GLOSSARIO

| Termine | Definizione |
|---|---|
| RAD | Documento di Analisi dei Requisiti. |
| SDD | Documento di Progettazione del Software. |
| FR | Requisito funzionale. |
| NFR | Requisito non funzionale. |
| API | Interfaccia di programmazione applicativa. |
| Dato valido | Informazione non scaduta secondo la policy della relativa fonte. |
| Sconosciuto | Stato usato quando manca un dato valido sufficiente per determinare l’accessibilità. |
| Tratto non verificato | Tratto senza dati sufficienti e validi per determinare la compatibilità. |
| Codice di tracking | Codice non enumerabile usato per consultare lo stato di una segnalazione. |
| Moderazione | Processo di valutazione e decisione su una segnalazione. |
| Duplicato | Segnalazione riferita a un caso già registrato e collegata senza cancellare la cronologia. |
| p95 | Valore sotto il quale ricade il 95 per cento delle misurazioni osservate. Popolazione e finestra temporale vanno definite nel protocollo. |
