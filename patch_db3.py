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

with open("runtime/stdlib/modules/database_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("args[0].to_python()", "(args[0].to_python() if hasattr(args[0], 'to_python') else args[0])")
content = content.replace("args[1].to_python()", "(args[1].to_python() if hasattr(args[1], 'to_python') else args[1])")

with open("runtime/stdlib/modules/database_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched database_lib.py")
