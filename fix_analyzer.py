import re

with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('("keys", 1)', '("keys", 1), ("map::keys", 1)')
content = content.replace('("len", 1)', '("len", 1), ("list::length", 1)')

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(content)
