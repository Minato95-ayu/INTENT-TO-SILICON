import pytest
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.instructions import Instruction, OpCode
from aayu.runtime.values.number import NumberValue
from aayu.runtime.values.string import StringValue

def test_vm_math_flow_e2e():
    vm = VirtualMachine()
    
    # Test ADD: 10 + 20
    vm.code = [
        Instruction(OpCode.PUSH_CONST, NumberValue(10)),
        Instruction(OpCode.PUSH_CONST, NumberValue(20)),
        Instruction(OpCode.ADD),
        Instruction(OpCode.HALT)
    ]
    vm.run()
    assert vm.stack.pop().value == 30
    
    # Test CONCAT: "Hello " + "World"
    vm = VirtualMachine()
    vm.code = [
        Instruction(OpCode.PUSH_CONST, StringValue("Hello ")),
        Instruction(OpCode.PUSH_CONST, StringValue("World")),
        Instruction(OpCode.ADD),
        Instruction(OpCode.HALT)
    ]
    vm.run()
    assert vm.stack.pop().value == "Hello World"
