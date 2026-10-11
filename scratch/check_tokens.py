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

import sys
import os

# Add local directory to path
sys.path.insert(0, os.path.abspath('.'))

from compiler.lexer.lexer import Lexer

with open("examples/whatsapp_clone/main.aayu", "r") as f:
    source = f.read()

lexer = Lexer(source)
for t in lexer.tokenize():
    print(t)