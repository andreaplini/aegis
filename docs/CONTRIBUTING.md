# Contribuire ad aegis

## Stato e ambito

Il repository contiene la documentazione RAD/SDD e l’esportazione DOCX. L’applicazione non è ancora implementata e non dispone di build o test applicativi. Seguire la [roadmap](MILESTONES.md) per distinguere attività completate, pianificate e decisioni aperte.

## Flusso di lavoro

1. Aprire o aggiornare un’attività descrivendo problema, attore, risultato atteso, criteri di accettazione e requisiti collegati. È possibile copiare il [modello di issue](template/ISSUE.md).
2. Lavorare su un branch dedicato e aprire una pull request verso `main`. Non riscrivere la cronologia condivisa e non inserire segreti o dati personali nel repository o nelle issue.
3. Aggiornare RAD per modifiche di requisito o comportamento. Aggiornare SDD per modifiche architetturali o operative. Registrare le decisioni architetturali in un ADR, mantenendo esplicito lo stato di approvazione.
4. Collegare ogni requisito funzionale interessato a casi d’uso, moduli e verifiche. Specificare come vengono verificate accessibilità, privacy e sicurezza quando la modifica le influenza.
5. Riportare nella pull request i controlli eseguiti e i risultati osservati. Non indicare test, prove con utenti, verifiche di ripristino o analisi non eseguite.

Per modifiche documentali applicare la skill [aegis-antislop](../.agents/skills/aegis-antislop/SKILL.md) insieme alla skill [aegis-docs](../.agents/skills/aegis-docs/SKILL.md). Controllare che ogni affermazione sia sostenuta da una fonte o marcata come proposta o decisione aperta, che i termini restino coerenti e che il diagramma globale riporti tutti i casi d’uso e le relative associazioni.

## Controlli disponibili

Per modifiche Markdown eseguire:

```sh
make check-docs
```

Il workflow `Verifica documentazione` esegue questo controllo per ogni push e pull request verso `main`, senza filtri sui percorsi. Il workflow `Genera documenti DOCX` esegue inoltre la generazione e validazione degli export quando cambiano i percorsi documentali configurati. La protezione remota di `main` non è ancora attiva, quindi il check non è attualmente un requisito di merge.

Il comando esegue i test del validatore e controlla percorsi e ancore locali, link esterni HTTPS, struttura numerata, ID roadmap, metadati e completezza degli ADR e la loro presenza in ENG-02, criteri e registri FR, corrispondenza dei responsabili FR con gli attori dei casi collegati, schema dei requisiti e del registro NFR nel template RAD, presenza dei glossari con intestazioni valide, definizioni complete e termini univoci, oggetti univoci nei modelli RAD e corrispondenza tra entity e diagramma delle classi, contratto di prenotazione idempotente prima degli effetti esterni tracciato tra UC-03, modello RAD, modello relazionale e SDD, ADR-0005 e ENG-06, completezza del registro revisioni e copertura di segnali, ripristino, recupero asincrono e moderazione nel runbook, campi FR/NFR inclusi responsabili dell’accettazione, esiti e riferimenti di evidenza, priorità, casi d’uso, descrizioni accessibili dei diagrammi in tutta la documentazione e tracciabilità tra RAD e moduli SDD. Verifica che ogni caso d’uso dichiarato compaia una sola volta nel diagramma globale e abbia un’associazione con ciascun attore partecipante dichiarato. Per verificare anche l’esportazione installare le versioni Node.js e Pandoc indicate in `config/tool-versions.env`. Installare i pacchetti Mermaid bloccati dal lockfile con `make install-doc-tools`, quindi eseguire:

```sh
make docs
```

I DOCX generati si trovano in `build/docs/` e non vanno aggiunti al repository. `make docs` verifica l’integrità del pacchetto, il contenuto richiesto, i metadati personali, nome e punteggiatura nel testo e nelle descrizioni alternative, le relazioni OOXML e le immagini dei diagrammi. Verifica anche la punteggiatura leggibile nel template Word e che `docs/template/assets/package/word/document.xml` corrisponda alla parte omonima del DOCX sorgente. Per modifiche applicative, eseguire i controlli della build e i test definiti quando ENG-03 introdurrà una build applicativa. Al momento tali comandi non esistono.

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
