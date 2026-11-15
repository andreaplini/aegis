---
name: aegis-docs
description: Create or revise Aegis RAD, SDD, template, and project documentation while preserving the supplied academic template and traceable requirements.
---

# Aegis documentation

Use for changes to `docs/RAD.md`, `docs/SDD.md`, `docs/template.md`, or related project documentation.

- Treat `docs/template.md` as the Markdown transcription of the source template and follow its section order. RAD sections cover introduction, current system, proposed system, user interface/prototype/usability, attachments, and glossary. SDD sections cover introduction, current system, proposed system, subsystem services, and glossary.
- Keep functional and non-functional requirements in tables. State an explicit actor/system action for functional requirements; give each non-functional requirement an action and an observable criterion. Include performance where relevant.
- Give use cases actors, preconditions, and postconditions. Preserve uncertainty as an explicit TBD rather than presenting an assumption as a fact.
- Write concise Italian prose suitable for an academic project. Remove filler, promotional claims, repeated context, and invented implementation status. Preserve technical terms where they are precise.
- Do not invent numeric thresholds, freshness periods, service levels, providers, or policy values. Identify the source and owner of each stated value; mark unresolved values as TBD. Distinguish source facts from calculated results and document the rule and inputs for derived values. Use stable names for requirements and domain concepts rather than duplicating subtly different labels.
- Keep Markdown files in `docs/`; link the source DOCX and extracted assets at their actual paths. Do not copy generated DOCX files into `docs/`.
