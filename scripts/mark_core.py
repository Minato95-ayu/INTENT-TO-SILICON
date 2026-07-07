import os

filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

phases_to_mark = [
    '[ ] **Advanced Playground Update**',
    '[ ] **Download Center & VS Code Realism**',
    '[ ] **The Big 3 Identities**'
]

for item in phases_to_mark:
    # Use a simpler replace in case of slight string mismatches
    content = content.replace(item, item.replace('[ ]', '[x]'))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md to mark Core Portals as done.")
