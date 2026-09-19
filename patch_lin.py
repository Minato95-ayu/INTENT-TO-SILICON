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
c = c.replace('self._emit("OP_ASYNC_CALL", ["print", 1])', 'self._emit("OP_ASYNC_CALL", ["print", 1])\n                self._emit("POP", [])')
with open("compiler/ir/linearizer.py", "w") as f:
    f.write(c)
