import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('- [ ] Formatter', '- [x] Formatter')
content = content.replace('- [ ] Linter', '- [x] Linter')
content = content.replace('- [ ] Production CLI', '- [x] Production CLI')
content = content.replace('- [ ] Language Server (LSP)', '- [x] Language Server (LSP)')
content = content.replace('- [ ] VS Code Extension Scaffold', '- [x] VS Code Extension Scaffold')
content = content.replace('- [ ] Tests & Demo', '- [x] Tests & Demo')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Stage 4 tasks.")
