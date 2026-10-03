import re

with open("runtime/stdlib/modules/map_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('.id', '')

with open("runtime/stdlib/modules/map_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
