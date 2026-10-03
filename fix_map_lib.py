import re

with open("runtime/stdlib/modules/map_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

def get_payload_fix(content):
    content = content.replace('args[0]._get_payload()', '(args[0]._get_payload() if hasattr(args[0], "_get_payload") else args[0])')
    return content

content = get_payload_fix(content)

with open("runtime/stdlib/modules/map_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
