import re
with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/tests/legacy/test_vm_errors.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\"Line: \d+\"', '\"Line: 1\"', text)
with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/tests/legacy/test_vm_errors.py', 'w', encoding='utf-8') as f:
    f.write(text)
