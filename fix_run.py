
with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("self._emit(Opcode.CALL_COMPONENT, 0)", "self._emit(Opcode.PREPARE_CALL, 0)\n            self._emit(Opcode.CALL, 0)")

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(code)

