import tracemalloc
import pytest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

def get_ast(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_memory_leak_vm_execution():
    source = """
    task main {
        let x = 10.
        let y = 20.
        let z = x + y.
    }
    """
    
    ast = get_ast(source)
    compiler = BytecodeEncoder()
    bytecode = compiler.compile(ast)
    
    vm = VirtualMachine()
    vm.code = bytecode
    
    # Warmup
    for _ in range(10):
        vm.run(bytecode)
        
    tracemalloc.start()
    
    snapshot1 = tracemalloc.take_snapshot()
    
    for _ in range(100):
        vm.run(bytecode)
        
    snapshot2 = tracemalloc.take_snapshot()
    
    tracemalloc.stop()
    
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    total_diff = sum(stat.size_diff for stat in stats)
    
    # Allow some small drift due to Python internals, but large leak should fail
    # 10KB drift across 100 executions is reasonable. 
    # If the VM was leaking its environments, it would be much larger.
    assert total_diff < 10000, f"Possible memory leak detected: {total_diff} bytes leaked across 100 executions"
