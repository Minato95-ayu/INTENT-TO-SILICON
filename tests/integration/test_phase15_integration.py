import sys, os
import pytest
sys.path.insert(0, os.path.abspath('.'))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig

def run_aayu_code(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    sem = SemanticAnalyzer().analyze(ast)
    pipe = IRPipeline()
    prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))
    
    config = VMConfig(debug_mode=False, enable_assertions=True)
    vm = VirtualMachine(config)
    vm.load(prog.bytecode, list(prog.constant_pool.values()), prog.action_addresses)
    
    # We call "main" if it exists
    if "main" in vm.action_addresses:
        vm.call_action_by_name("main")
    else:
        vm.execute()
    return vm

def test_dot_path_resolution():
    source = """
    action main()
        state my_data = {
            user: {
                name: "Ayush"
            }
        }
        
        state result = my_data.user.name
    end
    """
    vm = run_aayu_code(source)
    assert vm.state_scopes[0]["result"] == "Ayush"

def test_form_validation():
    source = """
    action main()
        state result = $form.valid
    end
    """
    vm = run_aayu_code(source)
    assert vm.state_scopes[0]["result"] == True # Default form is valid

def test_storage():
    source = """
    action main()
        storage.set("test_key", "test_value")
        state result = storage.get("test_key")
    end
    """
    vm = run_aayu_code(source)
    assert vm.state_scopes[0]["result"] == "test_value"
    
def test_http_get():
    source = """
    action main()
        state r = HTTP.get("https://jsonplaceholder.typicode.com/todos/1")
        state id = r.id
    end
    """
    vm = run_aayu_code(source)
    assert vm.state_scopes[0]["id"] == 1

def test_dup_opcode():
    config = VMConfig(debug_mode=False)
    vm = VirtualMachine(config)
    
    # 0x01 = PUSH_CONST
    # 0x03 = DUP
    # 0xFF = HALT
    vm.load(bytearray([0x01, 0x00, 0x00, 0x03, 0xFF]), ["Hello"])
    vm.execute()
    
    assert vm.value_stack.depth() == 2
    assert vm.value_stack.pop() == "Hello"
    assert vm.value_stack.pop() == "Hello"
