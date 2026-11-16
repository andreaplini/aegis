# Contribuire ad aegis

## Stato e ambito

Il repository contiene la documentazione RAD/SDD e l’esportazione DOCX. L’applicazione non è ancora implementata e non dispone di build o test applicativi. Seguire la [roadmap](MILESTONES.md) per distinguere attività completate, pianificate e decisioni aperte.

## Flusso di lavoro

1. Aprire o aggiornare un’attività descrivendo problema, attore, risultato atteso, criteri di accettazione e requisiti collegati. È possibile copiare il [modello di issue](template/ISSUE.md).
2. Lavorare su un branch dedicato e aprire una pull request verso `main`. Non riscrivere la cronologia condivisa e non inserire segreti o dati personali nel repository o nelle issue.
3. Aggiornare RAD per modifiche di requisito o comportamento; aggiornare SDD per modifiche architetturali o operative. Registrare le decisioni architetturali in un ADR, mantenendo esplicito lo stato di approvazione.
4. Collegare ogni requisito funzionale interessato a casi d’uso, moduli e verifiche. Specificare come vengono verificate accessibilità, privacy e sicurezza quando la modifica le influenza.
5. Riportare nella pull request i controlli eseguiti e i risultati osservati. Non indicare test, prove con utenti, verifiche di ripristino o analisi non eseguite.

## Controlli disponibili

Per modifiche Markdown eseguire:

```sh
make check-docs
```

Il comando esegue i test del validatore e controlla percorsi e ancore locali, struttura numerata, campi dei casi d’uso, tracciabilità degli ID FR/NFR/UC tra RAD e moduli SDD e stile del nome e della punteggiatura. Per verificare anche l’esportazione installare Pandoc 3.14, la versione fissata nella CI, ed eseguire:

```sh
make docs
```

I DOCX generati si trovano in `build/docs/` e non vanno aggiunti al repository. `make docs` verifica anche integrità del pacchetto, contenuto essenziale, nome e punteggiatura degli export. Per modifiche applicative, eseguire i controlli della build e i test definiti quando ENG-03 introdurrà una build applicativa; al momento tali comandi non esistono.

## Criteri di revisione

La revisione controlla che:

- requisiti, casi d’uso, codice, test e documentazione restino tracciabili;
- input esterni siano validati al confine e regole di dominio siano rappresentate con tipi e invarianti espliciti;
- dati assenti o scaduti non siano mostrati come prova di accessibilità;
- autorizzazioni e transizioni siano verificate lato server e gli effetti atomici siano coperti da test;
- log, esempi e fixture non contengano segreti, codici di tracking reali o dati personali;
- interfacce, viste testuali e flussi essenziali siano verificati con tastiera e tecnologie assistive;
- le verifiche riportate siano riproducibili e collegate all’ambiente e alla versione usati.

## Stato della governance GitHub

Verifica di sola lettura del repository `kairosci/aegis` il 16 novembre 2026:

| Controllo | Stato osservato |
|---|---|
| Visibilità e branch predefinito | Pubblico; `main` |
| Licenza dichiarata su GitHub | Non configurata |
| Issues | Abilitate |
| Protezione di `main` e ruleset | Non configurati |
| Avvisi di vulnerabilità Dependabot | Abilitati |
| Dependabot security updates | Abilitati |
| Secret scanning e push protection | Abilitati |
| Segnalazione privata delle vulnerabilità GitHub | Abilitata |
| Release | Nessuna release pubblicata |

La configurazione Dependabot apre pull request settimanali per gli aggiornamenti di versione delle GitHub Actions. Gli avvisi, gli aggiornamenti di sicurezza e la segnalazione privata delle vulnerabilità sono attivi. Per inviare una vulnerabilità usare la funzione privata nella pagina Security del repository, non le issue pubbliche. Il proprietario deve ancora decidere la licenza e i termini di contribuzione, la protezione di `main`, le review e gli status check obbligatori e la policy di merge.
