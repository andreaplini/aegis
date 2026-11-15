---
name: aegis-xml
description: Edit or validate XML used by Aegis, including Maven, Spring, OpenAPI, and document-related configuration.
---

# Aegis XML

Use when changing XML source or configuration files.

- Inspect the existing namespace declarations, schema location, encoding, and line endings before editing. Preserve them unless the requested change requires otherwise.
- Make a focused structural edit; do not rewrite or pretty-print an entire file when a localized change is sufficient.
- Keep XML well-formed and validate against the declared XSD or the owning tool when available. A parser-only check proves well-formedness, not schema validity.
- For XML derived from user input, disable external entity resolution and external DTD loading. Do not introduce external entities.
- Preserve comments, processing instructions, extension elements, and namespace-qualified names. Do not infer that unknown elements are safe to remove.
