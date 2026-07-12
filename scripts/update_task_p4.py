import os

task_path = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(task_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[/] Phase 4: Intent Engine & Offline NLP', '[x] Phase 4: Intent Engine & Offline NLP')
content = content.replace('[ ] Build real 	okenizer.py', '[x] Build real 	okenizer.py')
content = content.replace('[ ] Build real pos_tagger.py', '[x] Build real pos_tagger.py')

content = content.replace('[ ] Phase 5: Language Server (LSP)', '[/] Phase 5: Language Server (LSP)')

with open(task_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Phase 4")
