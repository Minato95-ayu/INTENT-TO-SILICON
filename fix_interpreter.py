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

with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('def op_ENTER_SCOPE(self, opcode):\n        self.vm.registers.ip += 1', 'def op_ENTER_SCOPE(self, opcode):\n        self.vm.registers.ip += 3')
c = c.replace('def op_EXIT_SCOPE(self, opcode):\n        self.vm.registers.ip += 1', 'def op_EXIT_SCOPE(self, opcode):\n        self.vm.registers.ip += 3')

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(c)
