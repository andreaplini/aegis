---
name: aegis-antislop
description: Keep aegis documentation concise, evidence-based, traceable, and free of invented claims.
---

# aegis anti-slop writing

Use this skill whenever creating, reviewing, or revising aegis documentation, diagrams, examples, or exports.

## Writing rules

- Name the actor, action, condition, result, and verification method where relevant.
- Label facts, proposals, approved decisions, open choices, and completed work accurately.
- Support claims with a repository artifact, authoritative source, owner decision, or recorded result.
- Remove unsupported claims. Never invent providers, data, research results, thresholds, policies, or readiness.
- For unresolved choices, name the owner and the evidence required to close the decision.
- Remove filler, promotion, vague praise, repeated context, and empty transitions.
- Keep detail that defines behavior, failure modes, invariants, boundaries, or verification.
- Use consistent names for requirements, actors, components, states, and data. Define acronyms once.
- Define domain and architecture terms in the document glossary when they affect behavior, data contracts, or failure handling.
- Keep one authoritative source for each decision. Link to it when summarizing elsewhere.
- Preserve supplied hierarchy, numbering, and source quotations. Do not rewrite user-owned material without authorization.
- Keep Markdown and human-readable text in DOCX deliverables and reference templates free of semicolons. Write the project name exactly as `aegis`.

## Requirements and diagrams

- Give each functional requirement an actor, observable action, priority, and defined use case. Define an acceptance criterion from the use-case flow and record the observed verification result with a link to evidence.
- Ensure every responsible actor named by a functional requirement participates in each use case linked to that requirement.
- Give each quality requirement an action, testable acceptance method, acceptance owner, observed result, and evidence reference. If governance has not appointed a person, record the accountable role and mark the appointment as pending. Mark unexecuted checks explicitly and never invent results.
- Give each use case actors, preconditions, postconditions, quality constraints, normal flow, and relevant alternatives or errors.
- Keep the overview diagram synchronized with the detailed cases. Show each use-case ID once, all participating human and external actors, and their associations.
- Ensure diagram labels, descriptions, flows, failure behavior, and requirements agree.
- Keep entity, boundary, and control catalogs free of duplicate identifiers and consistent with their diagrams and SDD counterparts.
- State how missing, stale, contradictory, partial, or unavailable data is represented and handled.
- For workflows crossing transaction boundaries, identify each authoritative store, the state exposed after partial failure, and the idempotent recovery or compensation path. Do not imply atomicity across systems that do not share a transaction.

## Review procedure

1. Read affected documents, linked requirements, models, and source evidence.
2. Check the status and source of each material claim. Correct, qualify, or remove unsupported claims.
3. Check repetition, vague wording, inconsistent terms, missing actors, failure paths, transaction boundaries, recovery behavior, and test evidence.
4. Edit the source documents and diagrams while preserving structure and user-owned material.
5. Run `make check-docs`. Run `make docs` when RAD, SDD, diagrams, export validation, or document tools change.
6. Review the diff and rendered exports. Confirm use-case coverage, alt descriptions, metadata, and embedded images.

Do not use a phrase blacklist or word count as a substitute for editorial judgment. Keep precise domain terms. Remove wording when it is unsupported, redundant, vague, promotional, or misleading.
