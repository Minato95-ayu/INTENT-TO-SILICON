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
pool = list(prog.constant_pool.values())
ip = 0
out = []
while ip < len(bytecode):
    opcode = bytecode[ip]
    name = [k for k, v in Opcode.__dict__.items() if v == opcode]
    name = name[0] if name else str(opcode)
    
    extra = ""
    if opcode in (Opcode.JMP, Opcode.JMP_IF_FALSE):
        target = bytecode[ip+1] | (bytecode[ip+2] << 8)
        extra = f" -> {target}"
    elif opcode == Opcode.LOAD_STATE or opcode == Opcode.STORE_STATE:
        idx = bytecode[ip+1] | (bytecode[ip+2] << 8)
        extra = f" {pool[idx]}"
    
    out.append(f'{ip}: {name}{extra}')
    if opcode in (Opcode.PUSH_CONST, Opcode.STORE_STATE, Opcode.LOAD_STATE, Opcode.JMP, Opcode.JMP_IF_FALSE, Opcode.CALL, Opcode.CREATE_MODEL, Opcode.REGISTER_ROUTE, Opcode.SETUP_EXCEPT, Opcode.SETUP_FINALLY, Opcode.LOAD_SUBSCR, Opcode.STORE_SUBSCR, Opcode.BUILD_DICT, Opcode.CREATE_ARRAY, Opcode.GET_LENGTH):
        ip += 3
    else:
        ip += 1
with open('disasm.txt', 'w') as f:
    f.write('\n'.join(out))
