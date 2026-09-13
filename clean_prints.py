
with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    code = f.read()

import re
code = re.sub(r"        print\(f\"\[ENCODER WIDGET TYPE\].*?\)\n", "", code)

with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("runtime/vm/validator.py", "r", encoding="utf-8") as f:
    code = f.read()

code = re.sub(r"            from runtime.vm.instructions import opcode_to_str\n            print\(f\"\[VAL TRACE\].*?\)\n", "", code)

with open("runtime/vm/validator.py", "w", encoding="utf-8") as f:
    f.write(code)

