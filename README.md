# Aegis

Monorepo per la piattaforma di mobilità urbana accessibile.

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/` | [RAD](docs/RAD.md), [SDD](docs/SDD.md), [modelli anonimizzati e riferimento Word](docs/template/) e [roadmap documentale](docs/MILESTONES.md). |
| `config/data/` | Dati e configurazioni del progetto. |
| `src/` | Codice applicativo. |
| `.agents/skills/` | Skill Codex specifiche del progetto. |
| `.github/workflows/` | Automazioni CI. |

La documentazione e tutti i relativi template e materiali di supporto risiedono in `docs/`. Il DOCX sorgente è il riferimento di stile e struttura; i DOCX esportati non sono versionati: il target `make docs` li genera in `build/docs/`. La GitHub Action esegue la stessa conversione e pubblica i due DOCX come artifact.

## Esportazione DOCX

Installare Pandoc e lanciare:

```sh
make docs
```

L'esportazione usa `docs/template/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX; MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
