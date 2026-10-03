import re

with open("runtime/stdlib/modules/core_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('registry.register("core::typeof", fn_typeof)', 'registry.register("core::typeof", fn_typeof)\n    registry.register("typeof", fn_typeof)')

with open("runtime/stdlib/modules/core_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
