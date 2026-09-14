import re

with open("runtime/stdlib/modules/database_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("args[0].to_python()", "(args[0].to_python() if hasattr(args[0], 'to_python') else args[0])")
content = content.replace("args[1].to_python()", "(args[1].to_python() if hasattr(args[1], 'to_python') else args[1])")

with open("runtime/stdlib/modules/database_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched database_lib.py")
