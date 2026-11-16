# aegis

Monorepo per la piattaforma di mobilità urbana accessibile.

## Stato del repository

Il repository contiene la baseline documentale e l'esportazione automatizzata di RAD e SDD. Il prodotto applicativo non è ancora implementato: `src/` non contiene moduli e non è presente una build applicativa. Requisiti e architettura descrivono il sistema proposto e restano da convalidare nei punti elencati in [RAD e SDD](docs/MILESTONES.md).

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/` | [RAD](docs/RAD.md), [SDD](docs/SDD.md), [modelli e riferimenti](docs/template.md), [roadmap](docs/MILESTONES.md) e [guida ai contributi](docs/CONTRIBUTING.md). |
| `config/` | Configurazione condivisa della toolchain, inclusa la versione Pandoc. |
| `config/data/` | Directory per i dati del progetto. Attualmente vuota. |
| `src/` | Codice applicativo. |
| `.agents/skills/` | Skill Codex specifiche del progetto. |
| `.github/` | Workflow CI, Dependabot e collegamento issue alla segnalazione privata delle vulnerabilità. |

La documentazione e tutti i relativi template e materiali di supporto risiedono in `docs/`. Il DOCX sorgente è il riferimento di stile e struttura. I DOCX esportati non sono versionati: il target `make docs` li genera e ne verifica archivio, contenuto e stile in `build/docs/`. La GitHub Action esegue lo stesso target e pubblica i due DOCX come artifact.

## Segnalazioni

Per bug e richieste, consultare le [issue aperte](https://github.com/kairosci/aegis/issues) e usare il [modello issue](docs/template/ISSUE.md) per descrivere contesto, riproduzione e risultato atteso. Per le vulnerabilità seguire la [politica di sicurezza](docs/SECURITY.md) e usare il report privato GitHub. Prima di condividere log o esempi, rimuovere credenziali, token, dati personali e codici di tracking.

## Esportazione DOCX

Installare la versione Pandoc indicata in `config/tool-versions.env` e lanciare:

```sh
make docs
```

La generazione esegue prima `make check-docs`, che verifica test del validatore, collegamenti e ancore locali, struttura dei modelli, completezza e unicità dei requisiti, tracciabilità RAD/SDD, casi d'uso e stile del progetto. Dopo la conversione controlla integrità, contenuto, nome e punteggiatura nei DOCX. `make check-docs` può essere lanciato separatamente e non richiede Pandoc.

`make docs` verifica anche che la versione locale di Pandoc corrisponda a quella configurata, così lo stesso convertitore viene usato localmente e in CI.

L'esportazione usa `docs/template/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX. MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
