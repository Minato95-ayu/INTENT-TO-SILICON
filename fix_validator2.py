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

with open('runtime/vm/validator.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('Opcode.SETUP_FINALLY, Opcode.EXEC_FINALLY):', 'Opcode.SETUP_FINALLY, Opcode.EXEC_FINALLY, Opcode.ENTER_SCOPE, Opcode.EXIT_SCOPE):')

with open('runtime/vm/validator.py', 'w', encoding='utf-8') as f:
    f.write(c)
