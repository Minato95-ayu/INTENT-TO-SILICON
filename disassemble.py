from runtime.vm.instructions import Opcode
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

with open('src/self_hosted/lexer.aayu', 'r') as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(sem_ast)
mir = pipeline.to_mir(hir)
lir = pipeline.to_lir(mir)
encoder = BytecodeEncoder()
prog = encoder.encode(lir)

bytecode = prog.bytecode
ip = 0
out = []
while ip < len(bytecode):
    opcode = bytecode[ip]
    name = [k for k, v in Opcode.__dict__.items() if v == opcode]
    name = name[0] if name else str(opcode)
    out.append(f'{ip}: {name}')
    if opcode in (Opcode.PUSH_CONST, Opcode.STORE_STATE, Opcode.LOAD_STATE, Opcode.JMP, Opcode.JMP_IF_FALSE, Opcode.CALL, Opcode.CREATE_MODEL, Opcode.REGISTER_ROUTE, Opcode.SETUP_EXCEPT, Opcode.SETUP_FINALLY, Opcode.LOAD_SUBSCR, Opcode.STORE_SUBSCR, Opcode.BUILD_DICT, Opcode.CREATE_ARRAY, Opcode.GET_LENGTH):
        ip += 3
    elif opcode == Opcode.CALL_METHOD:
        ip += 4
    elif opcode == Opcode.BINARY_OP:
        ip += 2
    else:
        ip += 1
with open('disasm.txt', 'w') as f:
    f.write('\n'.join(out))
