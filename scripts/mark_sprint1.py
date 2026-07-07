import os

filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
if not os.path.exists(filepath):
    filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\task.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('[ ]', '[x]')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Checked off all tasks in Sprint 1.")
