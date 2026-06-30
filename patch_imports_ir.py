import os
import glob

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("from ...ir", "from ir")
    content = content.replace("from ...errors", "from errors")
    content = content.replace("from ..ir", "from ir")
    content = content.replace("from ..errors", "from errors")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

vm_dir = r"prototype\language\runtime\vm"
for filepath in glob.glob(os.path.join(vm_dir, "*.py")):
    fix_file(filepath)

handlers_dir = os.path.join(vm_dir, "handlers")
for filepath in glob.glob(os.path.join(handlers_dir, "*.py")):
    fix_file(filepath)

print("Fixed ir and errors imports")
