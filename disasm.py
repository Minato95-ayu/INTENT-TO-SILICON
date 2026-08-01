from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.instructions import Opcode

source = open('ecommerce.aayu').read()
l = Lexer(source)
ast = Parser(l.tokenize()).parse()
ast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

# Disassemble bytecode
bc = prog.bytecode
pool = prog.constant_pool
i = 0
opcode_names = {v: k for k, v in vars(Opcode).items() if isinstance(v, int)}
while i < len(bc):
    op = bc[i]
    operand = (bc[i+1] << 8) | bc[i+2]
    name = opcode_names.get(op, f"UNKNOWN({op})")
    
    # Show pool value for PUSH_CONST
    extra = ""
    if name == "PUSH_CONST" and operand < pool.size():
        val = pool[operand]
        extra = f"  -> {repr(val)[:80]}"
    elif name == "BUILD_WIDGET":
        from aayu.compiler.bytecode.encoder import WIDGET_TYPES
        wt = {v: k for k, v in WIDGET_TYPES.items()}.get(operand, "?")
        extra = f"  -> {wt}"
    
    print(f"{i:4d}: {name:20s} {operand:5d}{extra}")
    i += 3
    if name == "HALT":
        break
