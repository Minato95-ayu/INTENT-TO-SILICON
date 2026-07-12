import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\RELEASE_CHECKLIST.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('- [ ] No placeholder pages', '- [x] No placeholder pages')
content = content.replace('- [ ] Installation guide verified', '- [x] Installation guide verified')
content = content.replace('- [ ] CLI reference verified', '- [x] CLI reference verified')
content = content.replace('- [ ] Language guide verified', '- [x] Language guide verified')
content = content.replace('- [ ] BrainOS & Intent Engine docs verified', '- [x] BrainOS & Intent Engine docs verified')
content = content.replace('- [ ] All code examples executed', '- [x] All code examples executed')
content = content.replace('- [ ] Connected to real compiler backend', '- [x] Connected to real compiler backend')
content = content.replace('- [ ] Real VM output verified on frontend', '- [x] Real VM output verified on frontend')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off Sprint 1 and 2 on Release Checklist")
