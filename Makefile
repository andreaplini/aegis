PANDOC ?= pandoc
OUTPUT_DIR ?= build/docs

.DEFAULT_GOAL := help
.PHONY: help check-docs docs

help:
	@printf '%s\n' \
	  'make docs       Generate and validate RAD and SDD DOCX files in $(OUTPUT_DIR)' \
	  'make check-docs  Test and validate docs, structure, traceability, and style' \
	  'Set PANDOC=/path/to/pandoc to select a Pandoc executable'

check-docs:
	python3 -m unittest discover -s tests
	python3 scripts/validate_docs.py

docs: check-docs
	$(MAKE) --no-print-directory $(OUTPUT_DIR)/rad-is.docx $(OUTPUT_DIR)/sdd-is.docx
	python3 scripts/validate_docx.py "$(OUTPUT_DIR)/rad-is.docx" "$(OUTPUT_DIR)/sdd-is.docx"

$(OUTPUT_DIR)/rad-is.docx: docs/RAD.md docs/template/template.docx scripts/validate_docx.py
	mkdir -p "$(OUTPUT_DIR)"
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx docs/RAD.md --output="$@"

$(OUTPUT_DIR)/sdd-is.docx: docs/SDD.md docs/template/template.docx scripts/validate_docx.py
	mkdir -p "$(OUTPUT_DIR)"
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx docs/SDD.md --output="$@"
