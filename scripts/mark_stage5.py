import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# AAYU v1.0 Roadmap

## 🚀 Stage 1: Website
- [x] Landing Page
- [x] Documentation
- [x] Playground
- [x] Download Center
- [x] Examples
- [x] Architecture Explorer
- [x] BrainOS Portal
- [x] Intent Engine Portal

## 🚀 Stage 2: BrainOS Intelligence
- [x] Cost Engine
- [x] Security Review
- [x] Performance Review
- [x] Architecture Review
- [x] Multi-domain reasoning
- [x] Automated Tests

## 🚀 Stage 3: Intent Engine
- [x] Offline NLP
- [x] Intent IR
- [x] Knowledge Graph
- [x] Clarification Engine
- [x] Architecture Integration
- [x] Unit & Integration Tests

## 🚀 Stage 4: Developer Tools
- [x] Formatter
- [x] Linter
- [x] Production CLI
- [x] Language Server (LSP)
- [x] VS Code Extension Scaffold
- [x] Tests & Demo

## 🚀 Stage 5: Release (Completed)
- [x] README, LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY
- [x] CHANGELOG, RELEASE_NOTES
- [x] Documentation Stubs (Installation, CLI, etc.)
- [x] CI/CD Actions Workflow
- [x] Benchmarks Script
- [x] Release Packager
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Stage 5 tasks.")
