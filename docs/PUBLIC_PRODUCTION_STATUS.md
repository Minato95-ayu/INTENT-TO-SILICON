# AAYU Public Production Status

## Honest current position

**AAYU is a working full-stack language prototype and developer toolchain.** It is suitable for learning, student projects, prototypes, local applications, controlled internal tools, and early MVPs. It is **not yet certified for unattended public-internet, company-level production workloads**.

This distinction matters: a working demo, a local deployment, and a production platform require different evidence. A public-production release needs repeatable operational, security, compatibility, and performance validation—not only feature implementation.

## What is verified now

The focused verification set below passes in this repository:

- 17 tests covering full-stack route handling, authentication-secret configuration, built-in imports, and C/Rust/Python/JavaScript interop.
- The VM HTTP router has bounded request bodies (1 MiB by default), per-client in-memory rate limiting, bearer-token verification hooks, request IDs, baseline response security headers, deterministic route errors, and clean shutdown.
- SQLite-backed models, pages, routes, built-in libraries, and explicit host-library bridges are implemented.

## What users can build today

- Hello World and programming practice
- Frontend pages and small full-stack apps
- HTTP routes and SQLite models
- Internal tools, prototypes, controlled APIs, and early developer projects
- Explicit bridges to C-ABI/native, Rust `cdylib`, Python, and JavaScript libraries

## Important boundaries

- AAYU currently runs on a Python-based compiler/VM. Do not claim C++-class performance or Rust-native memory safety until independently benchmarked and the native runtime is complete.
- Native, Rust, Python, and JavaScript bridges execute trusted host code with the process permissions. They are integration features, not a sandbox.
- The current rate limiter is in-memory and per process; it is not a distributed public-service control.
- TLS must terminate at a correctly configured reverse proxy or platform ingress. Do not expose the development server directly to the public internet.

## Requirements before public production certification

- TLS/HTTPS, secure headers, DNS, and reverse-proxy deployment guides tested end-to-end
- Complete authentication, authorization/RBAC middleware, session management, secret rotation, and audit trails
- Database migration workflow, backups, restoration drills, connection strategy, and recovery objectives
- Signed packages, dependency integrity checks, vulnerability management, and a published security-release process
- Structured logs, metrics, tracing, alerting, process supervision, graceful shutdown, and incident runbooks
- Load, soak, security, compatibility, and failure-recovery testing with published acceptance targets
- A green, reproducible full test suite across supported operating systems
- Complete exception/SSA pipeline, frontend forms/events, and the Rust-native compiler/runtime roadmap items

## Public wording to use now

> AAYU is a working full-stack programming-language prototype with production-oriented hardening. It is ready for learning, prototypes, local apps, and controlled internal services; public production deployment remains a hardening and validation milestone.

Do not market the project as “fully production-ready,” “Rust-native,” “C++-fast,” or “secure by default” until the relevant implementation and independent evidence exist.
