
with open("runtime/stdlib/stdlib.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("from .modules import (", "from .modules.ai_lib import register_ai_lib\n        from .modules import (")
code = code.replace("register_math_lib(self.registry)", "register_math_lib(self.registry)\n        register_ai_lib(self.registry)")

with open("runtime/stdlib/stdlib.py", "w", encoding="utf-8") as f:
    f.write(code)

