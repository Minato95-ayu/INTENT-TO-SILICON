import sys, os
sys.path.insert(0, os.path.abspath('.'))
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.instructions import Opcode

code = """
Page Counter
    state count = 0
    state msg = "Count is: "
    
    action inc()
        count = count + 1
        msg = "Count is: " + count
    end
    
    Column
        Text msg
        Button "Inc" onClick=inc
    end
end
"""
tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()
ast = SemanticAnalyzer().analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(ast)
mir = pipeline.to_mir(hir)
lir = pipeline.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

for name, addr in prog.action_addresses.items():
    print(f'Action {name} at {addr}')

idx = 0
while idx < len(prog.bytecode) - 2:
    op = prog.bytecode[idx]
    if op == Opcode.HALT: 
        print(f'{idx}: HALT')
        break
    try:
        op_name = next(k for k, v in Opcode.__dict__.items() if v == op and not k.startswith('_'))
    except StopIteration:
        op_name = str(op)
    arg = (prog.bytecode[idx+1] << 8) | prog.bytecode[idx+2]
    if op_name == 'PUSH_CONST':
        val = prog.constant_pool[arg]
        print(f'{idx}: {op_name} {arg} ({repr(val)})')
    elif op_name in ['INIT_STATE', 'STORE_VAR', 'LOAD_VAR']:
        val = prog.constant_pool[arg]
        print(f'{idx}: {op_name} {arg} ({repr(val)})')
    else:
        print(f'{idx}: {op_name} {arg}')
    idx += 3
