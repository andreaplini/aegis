# aegis

Monorepo per la piattaforma di mobilità urbana accessibile.

## Stato del repository

Il repository contiene la baseline documentale e l'esportazione automatizzata di RAD e SDD. Il prodotto applicativo non è ancora implementato: `src/` non contiene moduli e non è presente una build applicativa. Requisiti e architettura descrivono il sistema proposto e restano da convalidare nei punti elencati in [RAD e SDD](docs/MILESTONES.md).

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/` | [RAD](docs/RAD.md), [SDD](docs/SDD.md), [modelli e riferimenti](docs/template.md), [roadmap](docs/MILESTONES.md) e [guida ai contributi](docs/CONTRIBUTING.md). |
| `config/` | Configurazione condivisa della toolchain documentale e dei dati del progetto. |
| `config/data/` | Directory per i dati del progetto. Attualmente vuota. |
| `src/` | Codice applicativo. |
| `.agents/skills/` | Skill Codex specifiche del progetto. |
| `.github/` | Workflow CI, Dependabot e collegamento issue alla segnalazione privata delle vulnerabilità. |

La documentazione e tutti i relativi template e materiali di supporto risiedono in `docs/`. Il DOCX sorgente è il riferimento di stile e struttura. I DOCX esportati non sono versionati: il gate `make verify-docs` esegue audit, test, generazione e validazione in `build/docs/`. La GitHub Action usa lo stesso gate e pubblica i due DOCX come artifact.

## Segnalazioni

Per bug e richieste, consultare le [issue aperte](https://github.com/kairosci/aegis/issues) e usare il [modello issue](docs/template/ISSUE.md) per descrivere contesto, riproduzione e risultato atteso. Per le vulnerabilità seguire la [politica di sicurezza](docs/SECURITY.md) e usare il report privato GitHub. Prima di condividere log o esempi, rimuovere credenziali, token, dati personali e codici di tracking.

## Prerequisiti documentali

Per eseguire i controlli sono necessari Python `3.9` o successivo e GNU Make. La versione minima è definita in `config/tool-versions.env` e controllata da `make check-docs`. Il comando usa solo la libreria standard di Python e non richiede Node.js o Pandoc.

Per generare i DOCX servono anche Node.js `24.22.3` e Pandoc `3.14`, riportati in `config/tool-versions.env`. Installare queste versioni e renderle disponibili nel `PATH` prima di installare gli strumenti Mermaid. `make install-doc-tools` installa le dipendenze Node bloccate dal lockfile e Chromium headless. Non installa Node.js né Pandoc.

## Esportazione DOCX

Con i prerequisiti installati, predisporre Mermaid CLI e Chromium headless:

```sh
make install-doc-tools
```

Eseguire il gate documentale locale completo con:

```sh
make verify-docs
```

Il target esegue l’audit delle dipendenze, `make check-docs`, genera RAD e SDD e valida i DOCX. Per i soli controlli Markdown, senza Node.js o Pandoc, eseguire `make check-docs`. Per rigenerare gli export senza ripetere l’audit delle dipendenze, eseguire `make docs`. L’elenco dettagliato dei controlli è in [CONTRIBUTING](docs/CONTRIBUTING.md).

Mermaid CLI converte i diagrammi in immagini accessibili. Pandoc incorpora immagini e testo nei DOCX. Il validatore verifica pacchetto, contenuto, metadati, nome e punteggiatura nel testo e nelle descrizioni alternative, associazioni OOXML, immagini incorporate, punteggiatura del template Word e corrispondenza tra il DOCX sorgente e il file XML estratto versionato.

La CI esegue anche `make audit-doc-tools` sulle dipendenze degli strumenti documentali e blocca la generazione in presenza di vulnerabilità ad alta o critica gravità. Usa lo stesso target per ripetere il controllo in locale. Dependabot verifica settimanalmente gli aggiornamenti di Mermaid CLI e Puppeteer.

`make docs` verifica che Node.js e Pandoc corrispondano alle versioni configurate e Mermaid CLI alla versione dichiarata nel lockfile. La stessa toolchain viene usata localmente e in CI.

L'esportazione usa `docs/template/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX. MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
