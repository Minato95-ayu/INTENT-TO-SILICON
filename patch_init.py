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
with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    c = f.read()

patch = """    def op_INIT_STATE(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        name = self.vm.constant_pool[idx]
        val = self.vm.value_stack.pop()
        if not self.vm.state_scopes:
            from runtime.vm.exceptions import KernelError
            raise KernelError(f"state_scopes is empty at IP {self.vm.registers.ip - 3}")
        if name not in self.vm.state_scopes[-1]:
            self.vm.state_scopes[-1][name] = val
        return True"""

c = re.sub(r'    def op_INIT_STATE\(self, opcode\):.*?return True', patch, c, flags=re.DOTALL)
with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(c)
