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

with open("compiler/lexer/tokens.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"if", "else",', '"if", "elif", "else",')

with open("compiler/lexer/tokens.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Added elif to keywords")
