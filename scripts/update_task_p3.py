import os

task_path = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(task_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[/] Phase 3: BrainOS Real Intelligence', '[x] Phase 3: BrainOS Real Intelligence')
content = content.replace('[ ] Implement real AST scanning in production_review.py', '[x] Implement real AST scanning in production_review.py')
content = content.replace('[ ] Implement real load parameter logic in scaling_advisor.py', '[x] Implement real load parameter logic in scaling_advisor.py')
content = content.replace('[ ] Remove any remaining mock algorithms in BrainOS', '[x] Remove any remaining mock algorithms in BrainOS')

content = content.replace('[ ] Phase 4: Intent Engine & Offline NLP', '[/] Phase 4: Intent Engine & Offline NLP')

with open(task_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Phase 3")
