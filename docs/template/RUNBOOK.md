# Runbook operativo

Creare un runbook per servizio e ambiente. Completare i campi con procedure provate, collegamenti a fonti controllate e responsabili nominati. Non inserire credenziali, token o dati personali. Lasciare esplicitamente aperti gli obiettivi non approvati.

## Metadati

| Campo | Valore |
|---|---|
| Servizio e versione | Da compilare |
| Ambiente | Sviluppo / staging / produzione / altro da indicare |
| Responsabile operativo | Da designare |
| Escalation e copertura | Da concordare |
| Ultima revisione | Da compilare |
| Prossima revisione | Da concordare |

## Scopo e impatto

Descrivere le funzioni del servizio, gli utenti interessati, gli impatti di indisponibilità o dati non aggiornati e i servizi dipendenti. Collegare i requisiti e i criteri di servizio approvati.

## Accesso e prerequisiti

| Prerequisito | Metodo approvato | Responsabile o riferimento |
|---|---|---|
| Autorizzazione operativa | Da definire | Da designare |
| Configurazione e segreti | Riferimento a secret manager. Non copiarli qui | Da designare |
| Strumenti e dashboard | Da indicare | Da designare |
| Finestra di intervento e comunicazioni | Da concordare | Da designare |

## Segnali e diagnosi

| Sintomo o allarme | Evidenza da consultare | Criterio di escalation | Procedura collegata |
|---|---|---|---|
| Indisponibilità o latenza elevata | Metriche e log approvati | Soglia e responsabile da concordare | Da definire |
| Sincronizzazione fallita o dati scaduti | Esito, fonte e timestamp della sincronizzazione | Regola per fonte da approvare | Da definire |
| Coda di moderazione in crescita | Dimensione ed età della coda | Soglia e responsabile da concordare | Da definire |
| Errore di sicurezza o privacy | Audit e segnalazione controllata | Procedura di incidente da approvare | Da definire |

## Procedure operative

Documentare ogni procedura come sequenza numerata. Per ciascun passo indicare prerequisiti, comando o azione approvata, risultato atteso, criterio di arresto, conseguenze e metodo di verifica. Non includere comandi non provati sull’ambiente previsto.

### Rilascio e migrazione

Indicare controlli pre-rilascio, versione e provenienza degli artefatti, compatibilità della migrazione, approvazioni, verifica post-rilascio e criteri di rollback.

### Ripristino da backup

Indicare la fonte della copia, l’ambiente isolato, i passaggi di ripristino, la validazione d’integrità, i controlli applicativi e la registrazione dell’esito. Specificare l’obiettivo di punto di ripristino (Recovery Point Objective, RPO) e l’obiettivo di tempo di ripristino (Recovery Time Objective, RTO) solo dopo approvazione e misurazione.

### Sincronizzazione delle fonti

Descrivere avvio, retry, idempotenza, validazione, invalidazione cache e verifica dell’esito. In caso di fonte non valida o scaduta, mantenere i dati come sconosciuti e seguire la procedura di escalation approvata.

### Gestione degli incidenti

Descrivere rilevazione, classificazione, contenimento, escalation, comunicazioni, ripristino e revisione successiva. Indicare ruoli e canali approvati senza inserire dati personali o segreti.

## Verifiche e cronologia

| Data | Procedura provata | Ambiente e versione | Esito osservato | Problemi e follow-up | Esecutore e revisore |
|---|---|---|---|---|---|
| Da raccogliere | Da provare | Da indicare | Non eseguito | Da raccogliere | Da designare |

## Riferimenti e dipendenze

Elencare dashboard, configurazioni, inventario delle dipendenze, ADR, procedure collegate e contatti operativi approvati. Usare link a sistemi controllati invece di copiare segreti o dati riservati.
