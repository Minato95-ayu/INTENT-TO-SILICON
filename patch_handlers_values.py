import os
import glob

handlers_dir = r"prototype\language\runtime\vm\handlers"
for filepath in glob.glob(os.path.join(handlers_dir, "*.py")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("from ..values", "from ...values")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Fixed values imports in handlers")
