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

c = c.replace('elif mir.opcode == "POP_EXCEPT":\n            lir_list.append(LIRNode("POP_EXCEPT", []))', 'elif mir.opcode == "POP_EXCEPT":\n            lir_list.append(LIRNode("POP_EXCEPT", []))\n        elif mir.opcode == "ENTER_SCOPE":\n            lir_list.append(LIRNode("ENTER_SCOPE", []))\n        elif mir.opcode == "EXIT_SCOPE":\n            lir_list.append(LIRNode("EXIT_SCOPE", []))')

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(c)
