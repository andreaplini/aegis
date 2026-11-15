---
name: aegis-java
description: Design or implement Aegis Java and Jakarta EE code, including domain rules, use cases, REST adapters, persistence, and integrations.
---

# Aegis Java and Jakarta EE backend

Use when adding or changing Java code for the Aegis backend or workers.

- Follow the Java LTS version and Jakarta EE platform version configured by the repository; do not upgrade either as a side effect of a feature.
- Use Jakarta REST for HTTP resource adapters and the platform's dependency injection and persistence APIs where selected. Keep web resources thin; do not couple domain or application rules to Jakarta EE APIs.
- Organize code by domain (`places`, `accessibility`, `routing`, `reports`, `identity`, `integrations`) and keep domain, application, and adapter responsibilities distinct.
- Put invariants in domain objects. Prefer immutable value objects for identifiers, coordinates, source freshness, and validated inputs. Keep HTTP and persistence DTOs separate from domain types.
- Parse and validate untrusted strings, numbers, dates, coordinates, and enum tokens at adapter boundaries; pass domain types inward and serialize them explicitly at boundaries. Represent domain states with enums or sealed types, not scattered string comparisons. Derive values from canonical state instead of duplicating them; use named constants for genuine fixed domain rules and typed configuration for environment-dependent values. Never use silent fallback values that turn missing or stale accessibility data into accessible.
- Keep user-facing messages in message resources. Isolate fixed protocol, SQL, and framework tokens according to their contracts; do not dynamically assemble them to claim they are computed, and do not add abstraction for a single literal without a reuse or change-control need.
- Define application ports for repositories and external providers. Implement them in adapters; keep controllers thin and avoid god services or business rules in controllers.
- Put transactions around use cases that require atomic state changes. Keep slow network calls outside database transactions where possible; make retries and external effects explicit.
- Use constructor injection, explicit error handling, and names that state domain intent. Add or update tests for changed rules and transitions when the repository provides a test setup.
