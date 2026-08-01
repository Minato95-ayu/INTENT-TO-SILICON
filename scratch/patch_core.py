import re

with open('runtime/stdlib/modules/core_lib.py', 'r') as f:
    content = f.read()

content = content.replace('registry.register("core::print", fn_print)', 'registry.register("core::print", fn_print)\n    registry.register("print", fn_print)')

with open('runtime/stdlib/modules/core_lib.py', 'w') as f:
    f.write(content)
