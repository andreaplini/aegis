# aegis

Monorepo per la piattaforma di mobilità urbana accessibile.

## Stato del repository

Il repository contiene la baseline documentale e l'esportazione automatizzata di RAD e SDD. Il prodotto applicativo non è ancora implementato: `src/` non contiene moduli e non è presente una build applicativa. Requisiti e architettura descrivono il sistema proposto e restano da convalidare nei punti elencati in [RAD e SDD](docs/MILESTONES.md).

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/` | [RAD](docs/RAD.md), [SDD](docs/SDD.md), [modelli e riferimenti](docs/template.md), [roadmap](docs/MILESTONES.md) e [guida ai contributi](docs/CONTRIBUTING.md). |
| `config/data/` | Dati e configurazioni del progetto. |
| `src/` | Codice applicativo. |
| `.agents/skills/` | Skill Codex specifiche del progetto. |
| `.github/workflows/` | Automazioni CI. |

La documentazione e tutti i relativi template e materiali di supporto risiedono in `docs/`. Il DOCX sorgente è il riferimento di stile e struttura; i DOCX esportati non sono versionati: il target `make docs` li genera e ne verifica archivio, contenuto e stile in `build/docs/`. La GitHub Action esegue lo stesso target e pubblica i due DOCX come artifact.

## Segnalazioni

Per bug e richieste, consultare le [issue aperte](https://github.com/kairosci/aegis/issues) prima di inviarne una nuova. Per segnalare una vulnerabilità, non aprire un'issue pubblica: usare la funzione privata nella scheda Security del repository. Prima di condividere log o esempi, rimuovere credenziali, token, dati personali e codici di tracking.

## Esportazione DOCX

Installare Pandoc 3.14, la stessa versione fissata nella CI, e lanciare:

```sh
make docs
```

La generazione esegue prima `make check-docs`, che verifica test del validatore, collegamenti e ancore locali, struttura dei modelli, tracciabilità RAD/SDD, casi d'uso e stile del progetto. Dopo la conversione controlla integrità, contenuto, nome e punteggiatura nei DOCX. `make check-docs` può essere lanciato separatamente e non richiede Pandoc.

L'esportazione usa `docs/template/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX; MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
