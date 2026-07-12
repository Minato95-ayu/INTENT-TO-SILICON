# CLI Commands

AAYU ships as a command-line tool for creating projects, generating applications, and testing the experimental runtime path.

## Install

```bash
pip install aayu
```

For local development from this repository:

```bash
pip install -e .
```

## Create a Project

```bash
aayu init hospital
```

This creates a starter project where your AAYU source lives under `src/`.

## Generate Software

```bash
aayu generate src/main.aayu
```

Expected output shape:

```text
generated/
|-- frontend/
|-- backend/
|-- database/
`-- docker-compose.yml
```

## Validate Source

```bash
aayu validate src/main.aayu
```

Use validation before generation when changing entities, relations, workflows, or pages.

## Experimental Runtime

The runtime is currently a prototype track, not the primary production story.

Sprint 35 verification:

```bash
python -m prototype.cli vm prototype/tests/demo_sprint35.aayu
```

Output:

```text
Founder
```

That verifies:

```text
AAYU Source -> Parser -> Compiler -> AYC -> VM -> Execution
```
