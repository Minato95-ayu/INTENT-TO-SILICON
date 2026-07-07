import os

task_path = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(task_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[/] Phase 1: Standard Library Realization', '[x] Phase 1: Standard Library Realization')
content = content.replace('[ ] Implement real concurrency_lib.py', '[x] Implement real concurrency_lib.py')
content = content.replace('[ ] Implement real crypto_lib.py (with bcrypt dependency check)', '[x] Implement real crypto_lib.py (with bcrypt dependency check)')
content = content.replace('[ ] Phase 2: Playground & FastAPI Backend', '[/] Phase 2: Playground & FastAPI Backend')

with open(task_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md")
