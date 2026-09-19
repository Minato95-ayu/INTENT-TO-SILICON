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
with open("tests/vm/test_r6_1_c_runtime_abi.py", "r") as f:
    c = f.read()
c = re.sub(r'\"Stack depth mismatch on return\. Expected (\d+), got (\d+)\"', r'"Stack depth mismatch on (?:RETURN_VALUE|RET): expected \1, got \2"', c)
c = c.replace('"RET used but expected 0 returns"', '"RET used but expected 0 returns"')
with open("tests/vm/test_r6_1_c_runtime_abi.py", "w") as f:
    f.write(c)
