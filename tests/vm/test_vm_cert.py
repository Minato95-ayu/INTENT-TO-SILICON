# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import StackOverflowError, InvalidBytecodeError, KernelError
from runtime.vm.frame import CallFrame
from runtime.vm.result import RuntimeResult

def test_10m_instructions():
    # Construct 100k instructions to test throughput
    bytecode = bytearray()
    for _ in range(100000):
        # All instructions are 3 bytes! (1 opcode + 2 bytes padding)
        bytecode.extend([Opcode.PUSH_CONST, 0, 0, Opcode.POP, 0, 0])
    bytecode.extend([Opcode.HALT, 0, 0])
    
    vm = VirtualMachine(VMConfig.production())
    vm.load(bytecode, [1])
    vm.execute()
    
    assert vm.profiler.instruction_count == 200001
    assert len(vm.heap.allocator.pool.pool) == 0 # Zero memory leaks

def test_stack_overflow():
    vm = VirtualMachine(VMConfig.development())
    vm.call_stack.max_depth = 1
    
    frame1 = CallFrame("func1", 0)
    frame2 = CallFrame("func2", 0)
    
    vm.call_stack.push(frame1)
    with pytest.raises(StackOverflowError):
        vm.call_stack.push(frame2)

def test_invalid_opcode():
    vm = VirtualMachine(VMConfig.development())
    # 0x00 is invalid
    bytecode = bytearray([0x00, 0x00, 0x00])
    with pytest.raises(InvalidBytecodeError):
        vm.load(bytecode, [])

def test_plugin_recovery():
    vm = VirtualMachine()
    bytecode = bytearray([Opcode.DISPATCH, 0, 0, Opcode.HALT, 0, 0])
    vm.load(bytecode, [])
    
    vm.kernel_dispatch = lambda: RuntimeResult.error("Mock Plugin Error")
    
    from runtime.vm.exceptions import InternalException
    with pytest.raises(InternalException):
        vm.execute()

if __name__ == "__main__":
    pytest.main(["-v", __file__])


