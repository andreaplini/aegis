---
name: aegis-jsp
description: Build or revise Aegis server-rendered JSP views and their integration with web controllers.
---

# Aegis JSP views

Use when changing JSP pages, tags, or their controller-to-view contract. Do not introduce JSP solely because this skill exists; use it only when JSP is part of the selected frontend architecture or the task requests it.

- Keep request handling and business rules in controllers/use cases; JSP renders the supplied view model and does not access persistence or integrations.
- Use JSTL and Expression Language instead of Java scriptlets. Escape untrusted values for their output context; do not emit user content as raw HTML.
- Keep forms labeled and usable by keyboard and screen readers. Preserve validation messages, focus behavior, and error states in the rendered page.
- Keep JavaScript and CSS in their existing external module/resource structure. Preserve CSRF protection and authorization requirements for state-changing forms.
- Follow the repository's existing view resolver, tag library, and naming conventions rather than introducing a second rendering pattern.
