# Contribuire ad aegis

## Stato e ambito

Il repository contiene la documentazione RAD/SDD e l’esportazione DOCX. L’applicazione non è ancora implementata e non dispone di build o test applicativi. Il repository è pubblico ma non dichiara una licenza. Finché OPEN-10 non è risolta, non inviare contributi esterni che richiedono diritti di riuso o ridistribuzione. Consultare la proposta [ADR-0008](adr/ADR-0008-repository-license-and-contributions.md). Seguire la [roadmap](MILESTONES.md) per distinguere attività completate, pianificate e decisioni aperte.

## Flusso di lavoro

1. Aprire o aggiornare un’attività descrivendo problema, attore, risultato atteso, criteri di accettazione e requisiti collegati. È possibile copiare il [modello di issue](template/ISSUE.md).
2. I maintainer lavorano su un branch dedicato e aprono una pull request verso `main`. Chi segnala un problema può usare le issue abilitate. Non riscrivere la cronologia condivisa e non inserire segreti o dati personali nel repository o nelle issue.
3. Aggiornare RAD per modifiche di requisito o comportamento. Aggiornare SDD per modifiche architetturali o operative. Registrare le decisioni architetturali in un ADR, mantenendo esplicito lo stato di approvazione.
4. Collegare ogni requisito funzionale interessato a casi d’uso, moduli e verifiche. Specificare come vengono verificate accessibilità, privacy e sicurezza quando la modifica le influenza.
5. Riportare nella pull request i controlli eseguiti e i risultati osservati. Non indicare test, prove con utenti, verifiche di ripristino o analisi non eseguite.

Per modifiche documentali applicare la skill [aegis-antislop](../.agents/skills/aegis-antislop/SKILL.md) insieme alla skill [aegis-docs](../.agents/skills/aegis-docs/SKILL.md). Controllare che ogni affermazione sia sostenuta da una fonte o marcata come proposta o decisione aperta, che i termini restino coerenti e che il diagramma globale riporti tutti i casi d’uso e le relative associazioni.

## Controlli disponibili

I prerequisiti per i gate locali e le versioni richieste per l'esportazione sono descritti nei [prerequisiti documentali del README](../README.md#prerequisiti-documentali).

Per modifiche Markdown eseguire:

```sh
make check-docs
```

Il workflow `Verifica documentazione` esegue questo controllo per ogni push e pull request verso `main`, senza filtri sui percorsi. Il workflow `Genera documenti DOCX` esegue inoltre la generazione e validazione degli export quando cambiano i percorsi documentali configurati. La protezione remota di `main` non è ancora attiva, quindi il check non è attualmente un requisito di merge.

Il comando esegue i test del validatore e controlla:

- link locali, ancore, link HTTPS, struttura numerata, ID e dipendenze della roadmap, metadati e completezza degli ADR
- requisiti FR e NFR, attori partecipanti, priorità, criteri di accettazione e corrispondenza con i casi d’uso
- tracciabilità tra RAD e moduli SDD, copertura dei casi nel diagramma globale e associazione di ogni caso ai suoi attori
- corrispondenza tra le entità principali e il diagramma delle classi, mappatura delle entità a casi d’uso esistenti e presenza dei boundary e control catalogati nei diagrammi di sequenza
- contratto di prenotazione idempotente prima degli effetti esterni tra UC-03, RAD, modello relazionale, SDD, ADR-0005 ed ENG-06
- glossari, unicità dei nomi negli oggetti RAD, registro revisioni e copertura operativa del runbook
- descrizioni accessibili dei diagrammi in tutta la documentazione e stile canonico del nome del progetto

Per eseguire in locale l’audit delle dipendenze, i controlli documentali e l’esportazione validata, installare le versioni Node.js e Pandoc indicate in `config/tool-versions.env`, installare i pacchetti Mermaid bloccati dal lockfile con `make install-doc-tools` ed eseguire:

```sh
make verify-docs
```

Il comando esegue `make audit-doc-tools` e `make docs`. Gli export vengono salvati in `build/docs/` e non vanno aggiunti al repository. `make docs` verifica l’integrità del pacchetto, il contenuto richiesto, i metadati personali, nome e punteggiatura nel testo e nelle descrizioni alternative, le relazioni OOXML e le immagini dei diagrammi. Verifica anche la punteggiatura leggibile nel template Word e che `docs/template/assets/package/word/document.xml` corrisponda alla parte omonima del DOCX sorgente. Per modifiche applicative, eseguire i controlli della build e i test definiti quando ENG-03 introdurrà una build applicativa. Al momento tali comandi non esistono.

## Criteri di revisione

La revisione controlla che:

- requisiti, casi d’uso, codice, test e documentazione restino tracciabili,
- input esterni siano validati al confine e regole di dominio siano rappresentate con tipi e invarianti espliciti,
- dati assenti o scaduti non siano mostrati come prova di accessibilità,
- autorizzazioni e transizioni siano verificate lato server e gli effetti atomici siano coperti da test,
- log, esempi e fixture non contengano segreti, codici di tracking reali o dati personali,
- interfacce, viste testuali e flussi essenziali siano verificati con tastiera e tecnologie assistive,
- le verifiche riportate siano riproducibili e collegate all’ambiente e alla versione usati.

## Stato della governance GitHub

Verifica di sola lettura del repository `kairosci/aegis` il 16 novembre 2026:

| Controllo | Stato osservato |
|---|---|
| Visibilità e branch predefinito | Pubblico. Branch predefinito: `main` |
| Licenza dichiarata su GitHub | Non configurata |
| Issues | Abilitate |
| Protezione di `main` e ruleset | Non configurati |
| Avvisi di vulnerabilità Dependabot | Abilitati per le dipendenze rilevate |
| Dependabot security updates | Abilitati |
| Aggiornamenti Dependabot | GitHub Actions e strumenti Node documentali, controllo settimanale |
| Secret scanning e push protection | Abilitati |
| Rilevamento di pattern non provider | Disabilitato. Eleggibilità dell’account da verificare secondo ADR-0009. |
| Verifica di validità dei segreti rilevati | Disabilitata. L’invio dei segreti agli issuer e l’eleggibilità sono da approvare secondo ADR-0009. |
| Segnalazione privata delle vulnerabilità GitHub | Abilitata |
| Collegamento al report privato nel flusso issue | Configurato in `.github/ISSUE_TEMPLATE/config.yml` |
| Release | Nessuna release pubblicata |

La configurazione Dependabot apre pull request settimanali per gli aggiornamenti di versione delle GitHub Actions e degli strumenti Node documentali. La CI esegue `make audit-doc-tools` sugli strumenti e blocca la build per vulnerabilità ad alta o critica gravità. Lo stesso controllo può essere eseguito in locale. Gli avvisi, gli aggiornamenti di sicurezza e la segnalazione privata delle vulnerabilità sono attivi. Il flusso “New issue” mostra il collegamento al report privato e la [politica di sicurezza](SECURITY.md) ne descrive l'uso. Il proprietario deve ancora decidere la licenza e i termini di contribuzione secondo la proposta [ADR-0008](adr/ADR-0008-repository-license-and-contributions.md), la protezione di `main`, le review e gli status check obbligatori e la policy di merge.

La verifica delle impostazioni GitHub è stata eseguita in sola lettura il 16 novembre 2026. Gli endpoint sono relativi a `https://api.github.com`.

| Evidenza | Endpoint o artefatto | Risultato osservato |
|---|---|---|
| Visibilità, branch predefinito e licenza | `GET /repos/kairosci/aegis` tramite `gh repo view` | Pubblico, `main`, licenza assente. |
| Protezione del branch | `GET /repos/kairosci/aegis/branches/main/protection` | `404`, branch non protetto. |
| Ruleset | `GET /repos/kairosci/aegis/rulesets` | Elenco vuoto. |
| Avvisi di vulnerabilità | `GET /repos/kairosci/aegis/vulnerability-alerts` | Attivi, risposta positiva senza corpo. |
| Aggiornamenti di sicurezza Dependabot | `GET /repos/kairosci/aegis/automated-security-fixes` | `enabled: true`. |
| Scansione e protezione dei segreti | Proprietà `security_and_analysis` di `GET /repos/kairosci/aegis` | Scansione e push protection attive. Pattern non provider e controlli di validità disattivati. |
| Segnalazione privata delle vulnerabilità | `GET /repos/kairosci/aegis/private-vulnerability-reporting` | `enabled: true`. |
| Configurazione versionata | [.github/dependabot.yml](../.github/dependabot.yml) e [.github/ISSUE_TEMPLATE/config.yml](../.github/ISSUE_TEMPLATE/config.yml) | Aggiornamenti settimanali documentati e collegamento al report privato configurato. |

Questi risultati descrivono lo stato osservato in quella data e non sostituiscono la decisione del proprietario su OPEN-09, OPEN-10 e OPEN-11. Per i limiti di eleggibilità e gli effetti delle due impostazioni aggiuntive, consultare la proposta [ADR-0009](adr/ADR-0009-secret-scanning-eligibility-and-validity.md).
