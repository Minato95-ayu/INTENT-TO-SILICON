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

with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add a check for valid opcodes
patch = """
            elif opcode in (Opcode.GET_ITER, Opcode.FOR_ITER):
                # FOR_ITER will be replaced in R6.1-D, for now assume 0 stack effect conceptually for iteration
                pass
            else:
                raise InvalidBytecodeError(f"Unknown or unhandled opcode 0x{opcode:02X}", ip)
"""
content = re.sub(r'elif opcode in \(Opcode\.GET_ITER, Opcode\.FOR_ITER\):.*?pass', patch.strip(), content, flags=re.DOTALL)

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched validator.py to throw on invalid opcodes")
