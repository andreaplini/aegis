include config/tool-versions.env

export PANDOC_VERSION
PANDOC ?= pandoc
MERMAID ?= config/documentation/node_modules/.bin/mmdc
PUPPETEER ?= config/documentation/node_modules/.bin/puppeteer
PUPPETEER_CONFIG ?=
OUTPUT_DIR ?= build/docs
DOCX_TOOL_INPUTS = Makefile config/tool-versions.env config/documentation/package.json config/documentation/package-lock.json

.DEFAULT_GOAL := help
.PHONY: help install-doc-tools check-docs check-pandoc check-mermaid render-docs docs

help:
	@printf '%s\n' \
	  'make docs       Generate and validate RAD and SDD DOCX files in $(OUTPUT_DIR)' \
	  'make install-doc-tools  Install pinned Node tools and Chromium for Mermaid exports' \
	  'make check-docs  Test and validate docs, structure, traceability, and style' \
	  'make check-pandoc Check local Pandoc against config/tool-versions.env' \
	  'Set PANDOC and MERMAID to select alternate executables'

install-doc-tools:
	npm ci --prefix config/documentation
	npm exec --prefix config/documentation -- puppeteer browsers install chrome-headless-shell

check-docs:
	python3 -m unittest discover -s tests
	python3 scripts/validate_docs.py

check-pandoc:
	@version="$$($(PANDOC) --version | sed -n '1s/^pandoc //p')"; \
	if [ "$$version" != "$(PANDOC_VERSION)" ]; then \
	  printf 'Versione Pandoc richiesta: %s. Versione trovata: %s.\n' "$(PANDOC_VERSION)" "$$version" >&2; \
	  exit 1; \
	fi

check-mermaid:
	@expected="$$(node -p "require('./config/documentation/package.json').devDependencies['@mermaid-js/mermaid-cli']")"; \
	if [ ! -x "$(MERMAID)" ]; then \
	  printf 'Mermaid CLI non trovato. Eseguire npm ci --prefix config/documentation.\n' >&2; \
	  exit 1; \
	fi; \
	actual="$$($(MERMAID) --version)"; \
	if [ "$$actual" != "$$expected" ]; then \
	  printf 'Versione Mermaid CLI richiesta: %s. Versione trovata: %s.\n' "$$expected" "$$actual" >&2; \
	  exit 1; \
	fi; \
	browsers="$$($(PUPPETEER) browsers list)"; \
	if ! printf '%s\n' "$$browsers" | grep -q 'chrome-headless-shell@'; then \
	  printf 'Chromium headless non trovato. Eseguire make install-doc-tools.\n' >&2; \
	  exit 1; \
	fi

render-docs: check-mermaid
	mkdir -p "$(OUTPUT_DIR)"
	$(MERMAID) $(if $(PUPPETEER_CONFIG),--puppeteerConfigFile "$(PUPPETEER_CONFIG)") --input docs/RAD.md --output "$(OUTPUT_DIR)/rad-rendered.md" --outputFormat png --artefacts "$(OUTPUT_DIR)" --size 630 --jobs 1
	$(MERMAID) $(if $(PUPPETEER_CONFIG),--puppeteerConfigFile "$(PUPPETEER_CONFIG)") --input docs/SDD.md --output "$(OUTPUT_DIR)/sdd-rendered.md" --outputFormat png --artefacts "$(OUTPUT_DIR)" --size 630 --jobs 1

docs: check-docs check-pandoc
	$(MAKE) --no-print-directory $(OUTPUT_DIR)/rad-is.docx $(OUTPUT_DIR)/sdd-is.docx
	python3 scripts/validate_docx.py "$(OUTPUT_DIR)/rad-is.docx" "$(OUTPUT_DIR)/sdd-is.docx"

$(OUTPUT_DIR)/rad-is.docx: docs/RAD.md docs/template/template.docx scripts/validate_docx.py $(DOCX_TOOL_INPUTS) | render-docs
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx --resource-path=".:$(OUTPUT_DIR)" "$(OUTPUT_DIR)/rad-rendered.md" --output="$@"

$(OUTPUT_DIR)/sdd-is.docx: docs/SDD.md docs/template/template.docx scripts/validate_docx.py $(DOCX_TOOL_INPUTS) | render-docs
	$(PANDOC) --from=gfm --to=docx --standalone --reference-doc=docs/template/template.docx --resource-path=".:$(OUTPUT_DIR)" "$(OUTPUT_DIR)/sdd-rendered.md" --output="$@"
