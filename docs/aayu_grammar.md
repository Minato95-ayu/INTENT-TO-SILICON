# Aayu Grammar v0.1 — Formal Specification

## Overview

Aayu Grammar v0.1 is an **Architecture Definition Language (ADL)**, not a programming language. It represents the structural blueprint of a software ecosystem as a graph — domains, entities, features, and their relationships.

This grammar is the **formal output** of the Intent Lock phase. It captures "What are we building?" not "How are we building it?"

---

## Syntax

### 1. `system`

Declares the top-level system name. Exactly one per `.aayu` file.

```
system <Name>
```

Example:
```
system Adumate
```

---

### 2. `domains:`

A section listing all detected/confirmed domains. Each domain is indented on its own line.

```
domains:
  <domain_1>
  <domain_2>
  ...
```

Example:
```
domains:
  education
  housing
  employment
  library
```

---

### 3. `shared:`

A section listing entities that are shared across multiple domains. These are entities that appear in the `requires` graph of more than one detected domain.

```
shared:
  <entity_1>
  <entity_2>
  ...
```

Example:
```
shared:
  student
```

---

### 4. `entities:`

A section listing domain-specific entities that are NOT shared. These belong to a single domain's graph.

```
entities:
  <entity_1>
  <entity_2>
  ...
```

Example:
```
entities:
  room_allocation
  job_listing
  book_catalog
  borrow_record
```

---

### 5. `features:`

A section listing confirmed or inferred cross-cutting features (authentication, payments, notifications, etc.).

```
features:
  <feature_1>
  <feature_2>
  ...
```

Example:
```
features:
  payments
  notifications
```

---

### 6. `relations:`

A section listing directed relationships between entities. Uses `->` arrow syntax.

```
relations:
  <source> -> <target>
  ...
```

Example:
```
relations:
  student -> room_allocation
  student -> job_listing
  student -> book_catalog
```

---

## Complete Example: Adumate

```
system Adumate

domains:
  education
  housing
  employment
  library

shared:
  student

entities:
  enrollment
  academic_record
  course_content
  room_allocation
  job_listing
  application
  book_catalog
  borrow_record

features:
  payments
  notifications

relations:
  student -> enrollment
  student -> room_allocation
  student -> job_listing
  student -> book_catalog
```

---

## Rules

1. A `.aayu` file MUST have exactly one `system` declaration.
2. `domains:` MUST list at least one domain.
3. `shared:` is OPTIONAL. Only present if cross-domain entities exist.
4. `entities:` lists entities NOT already in `shared:`.
5. `features:` lists cross-cutting capabilities, not domain-specific entities.
6. `relations:` uses `->` to represent directed edges in the architecture graph.
7. All identifiers are `snake_case`.
8. Comments use `#` prefix.

---

## What This Grammar Does NOT Represent

- Implementation choices (database, framework, SDK)
- Control flow (loops, conditionals, functions)
- Data types or schemas
- API endpoints or routes

Those are downstream compiler stages, not ADL concerns.
