import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'
if not os.path.exists(filepath):
    filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('- [ ] Cost Engine', '- [x] Cost Engine')
content = content.replace('- [ ] Security Review', '- [x] Security Review')
content = content.replace('- [ ] Performance Review', '- [x] Performance Review')
content = content.replace('- [ ] Architecture Review', '- [x] Architecture Review')
content = content.replace('- [ ] Multi-domain reasoning', '- [x] Multi-domain reasoning')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Stage 2 tasks.")
