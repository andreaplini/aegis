# Aegis

Monorepo per la piattaforma di mobilità urbana accessibile.

## Struttura

| Percorso | Contenuto |
|---|---|
| `docs/` | Documentazione Markdown: RAD, SDD e trascrizione del template. |
| `templates/` | File sorgente usati come modelli. |
| `assets/` | Immagini e parti estratte dal template. |
| `config/data/` | Dati e configurazioni del progetto. |
| `src/` | Codice applicativo. |
| `.agents/skills/` | Skill Codex specifiche del progetto. |
| `.github/workflows/` | Automazioni CI. |

In `docs/` si mantengono solo file Markdown. I DOCX esportati non sono versionati: il target `make docs` li genera in `build/docs/`. La GitHub Action esegue la stessa conversione e pubblica i due DOCX come artifact.

## Esportazione DOCX

Installare Pandoc e lanciare:

```sh
make docs
```

L'esportazione usa `templates/template.docx` come riferimento di stile. Pandoc converte Markdown in DOCX; MarkItDown svolge la direzione opposta, da documenti sorgente a Markdown.
