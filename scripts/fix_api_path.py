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

﻿import os

api_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\api\main.py'
with open(api_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from language.lexer import Lexer", """
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from language.lexer import Lexer
""")

with open(api_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed sys.path")
