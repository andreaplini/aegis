---
name: aegis-javascript
description: Implement Aegis browser behavior, form interactions, and accessible progressive enhancement in JavaScript.
---

# Aegis JavaScript

Use when changing browser-side behavior or JavaScript modules.

- Follow the runtime and module setup already present. Do not add a framework, bundler, or dependency unless the task needs it and the repository's architecture supports it.
- Keep DOM behavior modular and tied to semantic controls. Preserve keyboard operation, visible focus, screen-reader status announcements, and usable error states.
- Treat browser input and server responses as untrusted. Use safe DOM sinks such as `textContent`; avoid building HTML from interpolated values.
- Handle loading, empty, success, and failure states explicitly. Do not make client-side validation a substitute for server validation.
- Keep presentation in CSS and domain decisions on the server. Avoid inline handlers and global mutable state when the existing structure permits modules.
