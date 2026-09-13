
import os

with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    enc_code = f.read()

patch = """        elif opcode == "DB_INSERT":
            idx = self.pool.add({"model": node.operands[0], "fields_count": node.operands[1]})
            self._emit(Opcode.DB_INSERT, idx)
        elif opcode == "DB_FIND":
            idx = self.pool.add(node.operands[0])
            self._emit(Opcode.DB_FIND, idx)
        elif opcode == "RESPOND":
            self._emit(Opcode.RESPOND, 0)
        elif opcode == "MARK_PAGE_START":"""

enc_code = enc_code.replace("        elif opcode == \"MARK_PAGE_START\":", patch)

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(enc_code)
print("Encoder patched!")

