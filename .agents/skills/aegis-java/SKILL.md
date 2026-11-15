---
name: aegis-java
description: Design or implement Aegis Java and Spring Boot code, including domain rules, use cases, REST adapters, persistence, and integrations.
---

# Aegis Java backend

Use when adding or changing Java code for the Aegis backend or workers.

- Follow the Java LTS version and Spring Boot version configured by the repository; do not upgrade either as a side effect of a feature.
- Organize code by domain (`places`, `accessibility`, `routing`, `reports`, `identity`, `integrations`) and keep domain, application, and adapter responsibilities distinct.
- Put invariants in domain objects. Prefer immutable value objects for identifiers, coordinates, source freshness, and validated inputs. Keep HTTP and persistence DTOs separate from domain types.
- Define application ports for repositories and external providers. Implement them in adapters; keep controllers thin and avoid god services or business rules in controllers.
- Put transactions around use cases that require atomic state changes. Keep slow network calls outside database transactions where possible; make retries and external effects explicit.
- Use constructor injection, explicit error handling, and names that state domain intent. Add or update tests for changed rules and transitions when the repository provides a test setup.
