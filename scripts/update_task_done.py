import os

filepath = r'C:\Users\ayush\.gemini\antigravity\brain\589c19e6-99f2-449b-ac95-e8c341c560c0\task.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Mark everything as done
content = content.replace('[ ]', '[x]')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated task.md.")
