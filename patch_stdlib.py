import os

stdlib_path = r"prototype\language\runtime\stdlib\stdlib.py"
with open(stdlib_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(".to_string()", ".stringify()")

with open(stdlib_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated stdlib.py stringify")
