---
name: aegis-project
description: Plan and implement changes that cross Aegis monorepo modules, build configuration, CI, or repository structure.
---

# Aegis project work

Use this skill for cross-module planning, repository layout, dependency changes, build and CI work, and project-level decisions.

- Inspect the current tree and existing conventions before choosing a location or adding a tool. The repository is a monorepo; do not create placeholder modules or duplicate an existing capability.
- Keep `docs/` for Markdown. The source template is `templates/template.docx`; extracted source assets belong under `assets/`. Generated DOCX files go to `build/` or CI artifacts, not `docs/`.
- Keep project data and configuration under the root `config/` tree; keep application source under `src/`.
- Make the smallest change that completes the requested work. Update the Makefile, workflow, README, or affected module boundaries only when the change requires it.
- Keep confirmed facts, decisions, and unresolved choices distinct. Mark unvalidated values as pending; do not invent providers, deployment targets, SLAs, or implemented features.
- Before finishing, check changed paths, references, ignore rules, and the relevant build or workflow. Do not rewrite Git history or publish/deploy without explicit authorization.
