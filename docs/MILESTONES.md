# Milestone documentali Aegis

## Ambito

La roadmap riguarda esclusivamente i documenti del progetto. Non pianifica né dichiara completati codice, infrastruttura, prototipi, prove con utenti o attività operative. Gli esiti di attività non svolte restano esplicitamente da raccogliere. Questo è l’unico file di milestone e roadmap del progetto.

Gli artefatti governati sono `docs/RAD.md`, `docs/SDD.md`, `docs/template/RAD.md`, `docs/template/SDD.md`, `docs/template.md`, il riferimento Word `docs/template/template.docx`, i materiali estratti in `docs/template/assets/` e le informazioni documentali in `README.md`.

## Roadmap

Gli sprint sono ordinati per dipendenza e non assegnano date o durate non concordate. Lo stato «Applicato» significa che l’intervento documentale e i relativi criteri sono stati completati; non sostituisce revisioni o prove che richiedono persone, fonti o ambienti esterni.

| Sprint | Obiettivo | Artefatti | Criterio di uscita | Stato |
|---|---|---|---|---|
| DOC-01 | Ricognizione della base documentale e dei vincoli | RAD, SDD, template, README | Inventario dei documenti esistenti; ambito documentale distinto da sviluppo e validazione sul campo. | Applicato |
| DOC-02 | Modelli anonimizzati e struttura accademica | Template RAD e SDD | Gerarchia completa dei modelli, campi riutilizzabili, nessun dato personale o risultato specifico dell’esempio. | Applicato |
| DOC-03 | Requisiti e confini del prodotto | RAD | Requisiti funzionali e non funzionali in tabelle con attore o sistema, azione, priorità e criterio osservabile; incertezze dichiarate. | Applicato |
| DOC-04 | Casi d’uso e tracciabilità | RAD | Attori, precondizioni e postcondizioni per ciascun caso; requisiti funzionali collegati ai casi d’uso, inclusa sincronizzazione. | Applicato |
| DOC-05 | Architettura e dati | SDD | Moduli, mappatura di distribuzione, persistenza, fonti, integrazioni, flussi, condizioni limite e servizi coerenti con i requisiti. | Applicato |
| DOC-06 | Accessibilità, usabilità, sicurezza e privacy | RAD e SDD | Requisiti e metodi di verifica documentati; nessun esito di test o punteggio inventato; decisioni non convalidate registrate. | Applicato |
| DOC-07 | Operatività e rilascio | RAD e SDD | Sincronizzazione, freschezza, monitoraggio, backup, incidenti, ambienti e processo di rilascio descritti con valori irrisolti marcati. | Applicato |
| DOC-08 | Revisione editoriale e consegna documentale | Tutti gli artefatti elencati | Struttura, collegamenti, terminologia e tracciabilità verificati; fonti e supporti documentali sono in `docs/`, mentre le esportazioni generate sono escluse dal versionamento. | Applicato |

## Applicazione degli sprint

| Sprint | Lavoro documentale applicato |
|---|---|
| DOC-01 | Conservata la trascrizione del template Word esistente come artefatto distinto e chiarito in `docs/template.md` dove si trovano i modelli specifici. Aggiornata la descrizione documentale in `README.md`. |
| DOC-02 | Creati i modelli RAD e SDD in `docs/template/`, mantenendo la gerarchia richiesta e sostituendo nomi, dati personali, servizi specifici e risultati del caso di esempio con campi o istruzioni generiche. |
| DOC-03 | Mantenute le tabelle FR e NFR del RAD. Ogni requisito funzionale ha un responsabile dell’azione, un’azione esplicita, una priorità e un collegamento al caso d’uso. I requisiti non funzionali riportano azione e criterio; performance è inclusa senza inventare soglie. |
| DOC-04 | Verificati attori, precondizioni e postcondizioni delle schede. Aggiunto `UC-06` per sincronizzazione e collegati i requisiti funzionali ai casi d’uso. Inclusi lo scenario e il diagramma di sequenza della sincronizzazione. |
| DOC-05 | Collegati moduli SDD e requisiti/casi d’uso; esplicitati catalogo delle fonti, cache geografica, provider di geocodifica, persistenza e adattatori. Le scelte non ancora approvate restano da convalidare. |
| DOC-06 | Esplicitati ascensori, rampe, accessi e annunci come caratteristiche consultabili. Uniformata la regola per cui dati assenti o scaduti sono sconosciuti. Il RAD mantiene metodo, misure individuali e aggregate, analisi, interviste e valutazione ISO senza risultati fittizi. |
| DOC-07 | Descritti ambienti separati, obiettivi di produzione, pipeline, compatibilità delle migrazioni, metriche e allarmi e requisiti per prove di ripristino e procedure incidenti. Runbook, soglie, responsabili e fornitori non concordati restano aperti. |
| DOC-08 | Controllati struttura, tracciabilità tra requisiti e architettura, collegamenti Markdown, coerenza del glossario e formattazione delle modifiche. Riferimento Word e materiali estratti sono mantenuti in `docs/template/`; generazione e pubblicazione degli export sono automatizzate. Le verifiche non dichiarano completate prove funzionali, accessibilità o ripristino. |

## Decisioni documentali ancora aperte

Questi elementi non impediscono di completare la stesura, ma devono essere risolti prima che la documentazione possa essere approvata come specifica definitiva o usata per dichiarare il servizio pronto al lancio.

| ID | Decisione o evidenza necessaria | Responsabile da designare | Evidenza di chiusura |
|---|---|---|---|
| OPEN-01 | Area pilota, operatori coinvolti, fonti autorizzate e responsabilità di aggiornamento. | Responsabile di prodotto con enti di trasporto | Ambito approvato e inventario delle fonti con responsabile per fonte. |
| OPEN-02 | Frequenza e validità delle caratteristiche, definizione di aggiornamento urgente e obiettivi di freschezza. | Responsabile dati con titolari delle fonti | Regole approvate e misurabili per fonte e tipo di dato. |
| OPEN-03 | Provider e rete per il routing accessibile, profili di esigenze supportati e comportamento del fallback. | Responsabile tecnico e referente mobilità | Decisione architetturale e criteri di compatibilità approvati. |
| OPEN-04 | Autenticazione, invio anonimo o autenticato, ruoli e accesso al tracking. | Responsabile prodotto e privacy | Policy di identità e autorizzazione approvate e riflesse nei casi d’uso. |
| OPEN-05 | Finalità, consenso, conservazione, accesso e cancellazione per identità, segnalazioni e immagini. | Responsabile privacy | Informativa e regole di trattamento approvate. |
| OPEN-06 | Standard e livello di conformità accessibile da adottare e protocollo delle prove con utenti. | Referente accessibilità con partecipanti e team di prodotto | Criteri approvati, sessioni svolte e risultati documentati nel RAD. |
| OPEN-07 | Target di performance, disponibilità, concorrenza, dimensione dei dati e obiettivi di ripristino. | Responsabile operativo | Soglie approvate e misure o prove registrate in ambiente concordato. |
| OPEN-08 | Runtime Java/Jakarta EE, provider gestiti, canali di notifica, dimensionamento e procedure di incidente. | Responsabile tecnico e operativo | Decisioni approvate, configurazioni per ambiente e procedure revisionate. |

## Criterio di completamento della roadmap

La roadmap documentale è applicata quando tutti gli sprint hanno raggiunto il criterio di uscita e gli artefatti sono coerenti tra loro. La documentazione resta una bozza finché le decisioni aperte non hanno un responsabile e un’evidenza di chiusura. I test con utenti, le verifiche tecniche, il ripristino dei backup e le misure operative sono attività future e non sono dichiarati svolti in questo piano.
