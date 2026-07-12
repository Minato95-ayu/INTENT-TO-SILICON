"""
=============================================================================
FILE: test_phase44_debugger.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys

# Ensure prototype directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine
from runtime.debugger.debugger import DebuggerRuntime
from runtime.debugger.host import MockDebuggerHost

def compile_source(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    compiler = AAYUCompiler()
    return compiler.compile(ast)

def test_breakpoint_pause():
    source = '''
    let x is 5.
    let y is 10.
    let z is x + y.
    '''
    bytecode = compile_source(source)
    
    host = MockDebuggerHost()
    debugger = DebuggerRuntime(host)
    vm = VirtualMachine(debugger=debugger)
    
    bp = debugger.breakpoint_manager.add_breakpoint("main", instruction_pointer=2)
    
    vm.run(bytecode)
    
    assert "PAUSED" in host.events
    assert "BREAKPOINT_1" in host.events
    assert host.paused[0]["ip"] == 2
    
    print("  [PASS] test_breakpoint_pause")

def test_step_into():
    source = '''
    let x is 5.
    let y is 10.
    let z is x + y.
    '''
    bytecode = compile_source(source)
    
    host = MockDebuggerHost()
    debugger = DebuggerRuntime(host)
    vm = VirtualMachine(debugger=debugger)
    
    bp = debugger.breakpoint_manager.add_breakpoint("main", instruction_pointer=0)
    
    def step_once(d, v):
        d.execution_controller.step_into()
        
    def resume(d, v):
        d.execution_controller.resume()
        
    host.queue_command(step_once)
    host.queue_command(resume)
    
    vm.run(bytecode)
    
    assert len(host.paused) == 2
    assert host.paused[0]["ip"] == 0
    assert host.paused[1]["ip"] == 1
    
    print("  [PASS] test_step_into")

def test_step_over():
    source = '''
    function my_func(a, b)
        return a + b.
    end.
    
    let x is my_func(5, 10).
    let y is x.
    '''
    bytecode = compile_source(source)
    
    host = MockDebuggerHost()
    debugger = DebuggerRuntime(host)
    vm = VirtualMachine(debugger=debugger)
    
    call_ip = None
    for i, inst in enumerate(bytecode.instructions):
        if inst.opcode.name == "CALL":
            call_ip = i
            break
            
    assert call_ip is not None
    
    bp = debugger.breakpoint_manager.add_breakpoint("main", instruction_pointer=call_ip)
    
    def step_over_cmd(d, v):
        d.execution_controller.step_over(len(v.frames))
        
    host.queue_command(step_over_cmd)
    
    vm.run(bytecode)
    
    assert len(host.paused) == 2
    assert host.paused[0]["ip"] == call_ip
    assert host.paused[1]["ip"] == call_ip + 1
    assert host.paused[0]["function"] == "main"
    assert host.paused[1]["function"] == "main"
    
    print("  [PASS] test_step_over")

def test_variable_inspector():
    source = '''
    let my_var is 42.
    let my_str is "hello".
    let z is 0.
    '''
    bytecode = compile_source(source)
    
    host = MockDebuggerHost()
    debugger = DebuggerRuntime(host)
    vm = VirtualMachine(debugger=debugger)
    
    bp = debugger.breakpoint_manager.add_breakpoint("main", instruction_pointer=4)
    
    inspected_vars = {}
    
    def inspect(d, v):
        nonlocal inspected_vars
        inspected_vars = d.variable_inspector.inspect_locals()
        d.execution_controller.resume()
        
    host.queue_command(inspect)
    vm.run(bytecode)
    
    assert "my_var" in inspected_vars, f"Variables were: {inspected_vars}"
    assert "my_str" in inspected_vars
    assert inspected_vars["my_var"] == 42
    assert inspected_vars["my_str"] == "hello"
    
    print("  [PASS] test_variable_inspector")

if __name__ == "__main__":
    print("\\n=== Phase 4.4 - Debugger Tests ===")
    test_breakpoint_pause()
    test_step_into()
    test_step_over()
    test_variable_inspector()
    print("--- All tests passed ---\\n")
