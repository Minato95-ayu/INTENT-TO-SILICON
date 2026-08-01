import re

with open('runtime/stdlib/modules/core_lib.py', 'r') as f:
    content = f.read()

content = content.replace('val = args[0].stringify() if args else ""', 'val = args[0].stringify() if args and hasattr(args[0], "stringify") else str(args[0]) if args else ""')

with open('runtime/stdlib/modules/core_lib.py', 'w') as f:
    f.write(content)
