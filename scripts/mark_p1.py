import os

filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

phases_to_mark = [
    '[ ] Hero me Live Project Generator ("Describe your app -> Build")',
    '[ ] "Build" animation',
    '[ ] Human Thought -> Intent Engine -> BrainOS -> AAYU -> Production pipeline',
    '[ ] Live architecture preview',
    '[ ] Real examples',
    '[ ] Zero fake stats'
]

for item in phases_to_mark:
    content = content.replace(item, item.replace('[ ]', '[x]'))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md for Phase 1.")
