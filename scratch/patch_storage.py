import re

with open('runtime/stdlib/modules/storage_lib.py', 'r') as f:
    content = f.read()

content = content.replace('data = vm.storage.get("__local__", {})', 'print("ARGS =", repr(args))\\n    data = vm.storage.get("__local__", {})')

with open('runtime/stdlib/modules/storage_lib.py', 'w') as f:
    f.write(content)
