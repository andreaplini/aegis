---
name: aegis-docs
description: Create or revise aegis RAD, SDD, template, and project documentation while preserving the supplied academic template and traceable requirements.
---

# aegis documentation

Use for changes to `docs/RAD.md`, `docs/SDD.md`, `docs/template.md`, or related project documentation.

- Follow the structure of the specific academic template or example documents supplied for the current task. When the user identifies example PDFs as the structural reference, mirror their section hierarchy and numbering in RAD/SDD; the generic transcription in `docs/template.md` is secondary for that task. Preserve the example's headings and section order while adapting domain content without copying its project-specific claims.
- Keep functional and non-functional requirements in tables. State an explicit actor/system action for functional requirements; give each non-functional requirement an action and an observable criterion. Include performance where relevant.
- Give use cases actors, preconditions, and postconditions. Preserve uncertainty as an explicit TBD rather than presenting an assumption as a fact.
- Write concise Italian prose suitable for an academic project. Remove filler, promotional claims, repeated context, and invented implementation status. Preserve technical terms where they are precise.
- Prefer Markdown prose and tables. Avoid decorative symbols and lists unless they improve structure or the template requires them. For every diagram or image, provide a concise text description of what it represents; do not put decorative numbering in images. Keep diagrams in Markdown-friendly formats when possible.
- Do not invent numeric thresholds, freshness periods, service levels, providers, or policy values. Identify the source and owner of each stated value; mark unresolved values as TBD. Distinguish source facts from calculated results and document the rule and inputs for derived values. Use stable names for requirements and domain concepts rather than duplicating subtly different labels.
- Keep Markdown files in `docs/`; link the source DOCX and extracted assets at their actual paths. Do not copy generated DOCX files into `docs/`.
