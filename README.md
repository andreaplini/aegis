# Mobilità urbana accessibile

Documenti di analisi dei requisiti (RAD) e di progettazione (SDD) per una web app di pianificazione della mobilità urbana accessibile.

## Documenti

- `docs/RAD.md`: requisiti e analisi.
- `docs/SDD.md`: architettura e progettazione.
- `docs/template.docx`: modello usato come riferimento grafico per l'esportazione.

## Esportare in DOCX

Installare [Pandoc](https://pandoc.org/installing.html), poi eseguire:

```sh
make docs
```

I file vengono creati in `build/docs/rad-is.docx` e `build/docs/sdd-is.docx`. GitHub Actions esegue la stessa conversione quando cambiano i Markdown o il template e pubblica i DOCX come artifact scaricabile dalla run.

MarkItDown è pensato per convertire documenti sorgente in Markdown. Per convertire Markdown in DOCX il progetto usa Pandoc.
