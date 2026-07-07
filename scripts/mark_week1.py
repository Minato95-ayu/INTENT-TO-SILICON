import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('- [ ] Intent Engine Portal (/intent-engine)', '- [x] Intent Engine Portal (/intent-engine)')
content = content.replace('- [ ] Architecture Explorer (/architecture)', '- [x] Architecture Explorer (/architecture)')
content = content.replace('- [ ] Examples Gallery (/examples)', '- [x] Examples Gallery (/examples)')
content = content.replace('- [ ] Playground Backend Integration (Connect UI to AST/Pipeline)', '- [x] Playground Backend Integration (Connect UI to AST/Pipeline)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Week 1 tasks.")
