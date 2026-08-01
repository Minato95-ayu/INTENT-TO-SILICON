from aayu.compiler.bytecode.decoder import BytecodeDecoder
from aayu.compiler.bytecode.disassembler import BytecodeDisassembler
program = BytecodeDecoder().decode('temp.aybc')
print(BytecodeDisassembler().disassemble(program))
