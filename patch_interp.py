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

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    c = f.read()

patch = """
    def op_DISPATCH(self):
        if hasattr(self.vm, 'kernel_dispatch'):
            res = self.vm.kernel_dispatch()
            if res.is_error():
                from runtime.vm.exceptions import KernelError
                self._throw_exception(KernelError(res.error_message))
                return
        self.vm.registers.ip += 3
"""

c = c.replace('class Interpreter:\n', 'class Interpreter:\n' + patch)
c = c.replace('self.dispatch_table[Opcode.EXEC_FINALLY] = self.op_EXEC_FINALLY', 'self.dispatch_table[Opcode.EXEC_FINALLY] = self.op_EXEC_FINALLY\n        self.dispatch_table[Opcode.DISPATCH] = self.op_DISPATCH')

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(c)
