import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('- [ ] Offline NLP (Tokenizer, POS, Entities, Actions)', '- [x] Offline NLP (Tokenizer, POS, Entities, Actions)')
content = content.replace('- [ ] Intent IR (JSON Output)', '- [x] Intent IR (JSON Output)')
content = content.replace('- [ ] Knowledge Graph (Domain Rules)', '- [x] Knowledge Graph (Domain Rules)')
content = content.replace('- [ ] Clarification Engine', '- [x] Clarification Engine')
content = content.replace('- [ ] Architecture Integration', '- [x] Architecture Integration')
content = content.replace('- [ ] Unit & Integration Tests', '- [x] Unit & Integration Tests')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Stage 3 tasks.")
