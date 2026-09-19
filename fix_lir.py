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

with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('"POP_EXCEPT", "THROW", "RETHROW"]:', '"POP_EXCEPT", "THROW", "RETHROW", "ENTER_SCOPE", "EXIT_SCOPE"]:')

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(c)
