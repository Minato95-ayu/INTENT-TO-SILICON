# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re
with open("compiler/ir/linearizer.py", "r") as f:
    c = f.read()

patch = """        if "." in name or "::" in name or name in BUILTIN_FUNCTIONS:
            self._emit("OP_ASYNC_CALL", [name, len(args)])
            if inst.result is None:
                self._emit("POP", [])
            else:
                self._pop_to(inst.result)
        else:
            return_count = 1 if inst.result is not None else 0
            self._emit("CALL_ACTION", [name, len(args), return_count])
            self._pop_to(inst.result)"""

c = re.sub(r'        if "\." in name or "::" in name or name in BUILTIN_FUNCTIONS:.*?        self\._pop_to\(inst\.result\)', patch, c, flags=re.DOTALL)
with open("compiler/ir/linearizer.py", "w") as f:
    f.write(c)
