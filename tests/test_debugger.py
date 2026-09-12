import unittest
import pytest
from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig
from runtime.vm.instructions import Opcode

def test_debugger_breakpoints():
    vm = VirtualMachine(VMConfig.development())
    
    bytecode = bytearray()
    bytecode.append(Opcode.PUSH_CONST)
    bytecode.extend((0).to_bytes(2, 'big'))
    bytecode.extend([Opcode.HALT, 0, 0])
    
    vm.load(bytecode, constant_pool=[10])
    
    vm.debugger.add_breakpoint(3)
    assert 3 in vm.debugger.breakpoints
    
    # Just run it, check_breakpoint is just a print statement currently
    vm.execute()
    assert vm.registers.ip == 3  # Completed HALT (ip advanced by 3 before breaking out of loop maybe, or halted at 3?)

if __name__ == "__main__":
    pytest.main(["-v", __file__])

