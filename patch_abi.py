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

with open("tests/vm/test_r6_1_c_runtime_abi.py", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'Stack depth mismatch on \(RETURN_VALUE\|RET\): expected (\d+), got (\d+)', r'Stack depth mismatch on return. Expected \1, got \2', content)

with open("tests/vm/test_r6_1_c_runtime_abi.py", "w", encoding="utf-8") as f:
    f.write(content)

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    interp = f.read()
interp = interp.replace("self.execute(", "self.run(")
with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(interp)
