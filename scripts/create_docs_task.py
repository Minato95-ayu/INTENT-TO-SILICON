import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

content = '''# Developer Operating System - Phase 3 (Documentation Portal)

## ✅ Priority 3 — Documentation Architecture
- [ ] **Global Docs Layout**: Mobile sidebar, Top Breadcrumbs.
- [ ] **Ctrl+K Search**: Interactive modal simulating search over Docs.
- [ ] **Docs Homepage (/docs)**: Beautiful grid showcasing Getting Started, Language, BrainOS, Intent Engine, API Ref.
- [ ] **Docs Components**:
  - [ ] Code Block (Syntax Highlighting, Copy, Run in Playground).
  - [ ] Visual Diagram Component (ASCII/Boxes for Pipeline).
  - [ ] Common Errors (Wrong vs Correct).
  - [ ] Authenticity Tag (e.g. "Edit on GitHub - Available in v1.0").
- [ ] **Core Content Pages ([...slug])**:
  - [ ] Render dynamic content (e.g., Syntax, Variables, AST, BrainOS).
  - [ ] Include Next/Previous Reading Order links.
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created new task list for Phase 3 (Documentation).")
