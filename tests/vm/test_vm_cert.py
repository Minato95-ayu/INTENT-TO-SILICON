import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from aayu.runtime.vm_next.vm import VirtualMachine
from aayu.runtime.vm_next.config import VMConfig
from aayu.runtime.vm_next.instructions import Opcode
from aayu.runtime.vm_next.exceptions import StackOverflowError, InvalidBytecodeError
from aayu.runtime.vm_next.frame import CallFrame

def test_10m_instructions():
    # Construct 100k instructions to test throughput (10M takes too long in python pytest usually without JIT)
    bytecode = bytearray()
    for _ in range(100000):
        bytecode.extend([Opcode.PUSH_CONST, 0, 0, Opcode.POP])
    bytecode.append(Opcode.HALT)
    
    vm = VirtualMachine(VMConfig.production())
    vm.load(bytecode, [1])
    vm.execute()
    
    assert vm.profiler.instruction_count == 200001
    assert len(vm.heap.allocator.pool.pool) == 0 # Zero memory leaks

def test_stack_overflow():
    vm = VirtualMachine(VMConfig.development())
    vm.load(bytearray([Opcode.HALT]), [])
    
    with pytest.raises(StackOverflowError):
        for _ in range(5000):
            vm.call_stack.push(CallFrame("func", 0))

def test_invalid_opcode():
    vm = VirtualMachine()
    bytecode = bytearray([0xFE]) # Unknown
    
    with pytest.raises(InvalidBytecodeError) as exc:
        vm.load(bytecode)
    assert "Unknown opcode" in str(exc.value)

def test_plugin_recovery():
    from aayu.runtime.vm_next.result import RuntimeResult, ResultStatus
    
    vm = VirtualMachine()
    # Mocking a dispatch instruction
    bytecode = bytearray([Opcode.DISPATCH, Opcode.HALT])
    vm.load(bytecode)
    
    # Mock kernel_dispatch to return ERROR
    vm.kernel_dispatch = lambda: RuntimeResult.error("Mock Plugin Error")
    
    # Execution should not crash, because interpreter catches KernelError and pushes None
    vm.execute()
    assert vm.value_stack.pop() is None

if __name__ == '__main__':
    pytest.main(['-v', __file__])
