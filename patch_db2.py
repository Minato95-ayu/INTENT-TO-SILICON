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

with open("runtime/stdlib/modules/database_lib.py", "r") as f:
    content = f.read()

content = content.replace("except Exception:", "except Exception as e:\n            print(f'DB Error: {e}')")

with open("runtime/stdlib/modules/database_lib.py", "w") as f:
    f.write(content)
