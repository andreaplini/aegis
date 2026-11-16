include config/tool-versions.env

export PANDOC_VERSION
PANDOC ?= pandoc
OUTPUT_DIR ?= build/docs

.DEFAULT_GOAL := help
.PHONY: help check-docs check-pandoc docs

help:
	@printf '%s\n' \
	  'make docs       Generate and validate RAD and SDD DOCX files in $(OUTPUT_DIR)' \
	  'make check-docs  Test and validate docs, structure, traceability, and style' \
	  'make check-pandoc Check local Pandoc against config/tool-versions.env' \
	  'Set PANDOC=/path/to/pandoc to select a Pandoc executable'

check-docs:
	python3 -m unittest discover -s tests
	python3 scripts/validate_docs.py

check-pandoc:
	@version="$$($(PANDOC) --version | sed -n '1s/^pandoc //p')"; \
	if [ "$$version" != "$(PANDOC_VERSION)" ]; then \
	  printf 'Versione Pandoc richiesta: %s. Versione trovata: %s.\n' "$(PANDOC_VERSION)" "$$version" >&2; \
	  exit 1; \
	fi

docs: check-docs check-pandoc
	$(MAKE) --no-print-directory $(OUTPUT_DIR)/rad-is.docx $(OUTPUT_DIR)/sdd-is.docx
	python3 scripts/validate_docx.py "$(OUTPUT_DIR)/rad-is.docx" "$(OUTPUT_DIR)/sdd-is.docx"

$(OUTPUT_DIR)/rad-is.docx: docs/RAD.md docs/template/template.docx scripts/validate_docx.py
	mkdir -p "$(OUTPUT_DIR)"
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx docs/RAD.md --output="$@"

$(OUTPUT_DIR)/sdd-is.docx: docs/SDD.md docs/template/template.docx scripts/validate_docx.py
	mkdir -p "$(OUTPUT_DIR)"
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx docs/SDD.md --output="$@"
