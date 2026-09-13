
import os
import re

with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    code = f.read()

# First remove the broken one I added
code = code.replace("""        elif opcode == "DB_INSERT":
            idx = self.pool.add({"model": node.operands[0], "fields_count": node.operands[1]})
            self._emit(Opcode.DB_INSERT, idx)
        elif opcode == "DB_FIND":
            idx = self.pool.add(node.operands[0])
            self._emit(Opcode.DB_FIND, idx)
        elif opcode == "RESPOND":
            self._emit(Opcode.RESPOND, 0)
        
    def _encode_state_init""", "    def _encode_state_init")

patch = """        elif opcode == "DB_INSERT":
            idx = self.pool.add({"model": node.operands[0], "fields_count": node.operands[1]})
            self._emit(Opcode.DB_INSERT, idx)
        elif opcode == "DB_FIND":
            idx = self.pool.add(node.operands[0])
            self._emit(Opcode.DB_FIND, idx)
        elif opcode == "RESPOND":
            self._emit(Opcode.RESPOND, 0)
        else:"""

code = code.replace("        else:\n            # Unknown LIR opcode", patch + "\n            # Unknown LIR opcode")

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Patched.")

