
import os

with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

for i, line in enumerate(lines):
    if line.strip() == "new_depth = depth":
        lines.insert(i+1, "            old_depth = new_depth")
        break

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Fixed trace!")

