import os

repo_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON'

files = {
    'README.md': '''# AAYU Programming Language (v1.0.0 Stable)

AAYU is an AI-native programming language and developer platform. It integrates a deterministic compiler with a semantic Intent Engine (BrainOS) to translate human architectural intents into secure, scalable, and optimized code.

## Key Features
- **Deterministic Syntax**: Strict, unambiguous syntax designed for AI inference.
- **BrainOS**: Multi-domain reasoning engine for architecture generation.
- **Intent Engine**: Offline NLP that parses human requirements into actionable JSON IR.
- **Zero-Cost Abstractions**: High-level abstractions that compile down to optimized bytecode.

## Installation
See \docs/installation.md\ for installation instructions on Windows, macOS, and Linux.

## Documentation
Full documentation is available in the \docs/\ directory and at https://aayu.dev.
''',
    
    'LICENSE': '''MIT License

Copyright (c) 2026 Ayush / Intent to Silicon Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
''',

    'CONTRIBUTING.md': '''# Contributing to AAYU

We love your input! We want to make contributing to AAYU as easy and transparent as possible.

## Pull Requests
1. Fork the repo and create your branch from main.
2. Ensure you run the linter and formatter using the AAYU CLI (ayu lint / ayu fmt).
3. Ensure the test suite passes (pytest prototype/tests/).
4. Issue that pull request!
''',

    'CODE_OF_CONDUCT.md': '''# Contributor Covenant Code of Conduct

## Our Pledge
We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone.
''',

    'SECURITY.md': '''# Security Policy

## Supported Versions
Only the latest major release (v1.x) receives active security updates.

## Reporting a Vulnerability
Please do not open public issues for security vulnerabilities. Email security@aayu.dev directly.
''',

    'CHANGELOG.md': '''# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-05
### Added
- Core Language: Parser, AST, Semantic Analyzer, Bytecode Generator, VM.
- BrainOS: Multi-domain reasoning, Cost Engine, Security Review.
- Intent Engine: Offline NLP tokenizer, Intent IR builder.
- Developer Tools: LSP, Linter, Formatter, VS Code extension.
''',

    'RELEASE_NOTES.md': '''# Release Notes: AAYU v1.0.0

AAYU 1.0.0 marks the first stable release of the AI-native developer platform.
This release includes the complete orchestration pipeline from Human Intent -> Intermediate Representation -> Logical Architecture -> Scaffolded Code.
'''
}

for filename, content in files.items():
    with open(os.path.join(repo_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\\n")

print("Generated Repository Polish Files.")
