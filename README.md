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

La documentazione e tutti i relativi template e materiali di supporto risiedono in `docs/`. Il DOCX sorgente è il riferimento di stile e struttura. I DOCX esportati non sono versionati: il target `make docs` li genera e ne verifica archivio, contenuto e stile in `build/docs/`. La GitHub Action esegue lo stesso target e pubblica i due DOCX come artifact.

## Segnalazioni

Per bug e richieste, consultare le [issue aperte](https://github.com/kairosci/aegis/issues) e usare il [modello issue](docs/template/ISSUE.md) per descrivere contesto, riproduzione e risultato atteso. Per le vulnerabilità seguire la [politica di sicurezza](docs/SECURITY.md) e usare il report privato GitHub. Prima di condividere log o esempi, rimuovere credenziali, token, dati personali e codici di tracking.

## Esportazione DOCX

Installare la versione Node.js e la versione Pandoc indicate in `config/tool-versions.env`, quindi predisporre Mermaid CLI e Chromium headless:

```sh
make install-doc-tools
```

Generare e verificare gli export con:

```sh
make docs
```

La generazione esegue prima `make check-docs`. Il comando esegue i test del validatore e controlla link, struttura, requisiti, tracciabilità RAD/SDD, casi d’uso e diagramma, completezza degli ADR e loro presenza in ENG-02, glossari, unicità degli oggetti RAD e corrispondenza tra entity e diagramma delle classi, copertura operativa del runbook, descrizioni accessibili e stile del nome. Il catalogo completo dei controlli è in [CONTRIBUTING](docs/CONTRIBUTING.md). Il comando può essere eseguito separatamente e non richiede Node.js o Pandoc.

Mermaid CLI converte i diagrammi in immagini accessibili. Pandoc incorpora immagini e testo nei DOCX. Il validatore verifica pacchetto, contenuto, metadati, nome e punteggiatura nel testo e nelle descrizioni alternative, associazioni OOXML, immagini incorporate, punteggiatura del template Word e corrispondenza tra il DOCX sorgente e il file XML estratto versionato.

La CI esegue anche `make audit-doc-tools` sulle dipendenze degli strumenti documentali e blocca la generazione in presenza di vulnerabilità ad alta o critica gravità. Usa lo stesso target per ripetere il controllo in locale. Dependabot verifica settimanalmente gli aggiornamenti di Mermaid CLI e Puppeteer.

`make docs` verifica che Node.js e Pandoc corrispondano alle versioni configurate e Mermaid CLI alla versione dichiarata nel lockfile. La stessa toolchain viene usata localmente e in CI.

L'esportazione usa `docs/template/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX. MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
