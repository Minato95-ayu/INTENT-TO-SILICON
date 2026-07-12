import os

task_path = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(task_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[/] Phase 5: Language Server (LSP)', '[x] Phase 5: Language Server (LSP)')
content = content.replace('[ ] Build real JSON-RPC handler', '[x] Build real JSON-RPC handler')
content = content.replace('[ ] Implement diagnostic/completion generation from compiler', '[x] Implement diagnostic/completion generation from compiler')

content = content.replace('[ ] Phase 6: Deep QA & Release', '[/] Phase 6: Deep QA & Release')

with open(task_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Phase 5")
