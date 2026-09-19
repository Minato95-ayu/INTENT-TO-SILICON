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

with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('elif opcode == "POP_EXCEPT":\n            self._emit(Opcode.POP_EXCEPT, 0)', 'elif opcode == "POP_EXCEPT":\n            self._emit(Opcode.POP_EXCEPT, 0)\n        elif opcode == "ENTER_SCOPE":\n            self._emit(Opcode.ENTER_SCOPE, 0)\n        elif opcode == "EXIT_SCOPE":\n            self._emit(Opcode.EXIT_SCOPE, 0)')

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(c)
