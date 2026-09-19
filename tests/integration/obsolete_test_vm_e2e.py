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
from runtime.vm.vm import VirtualMachine
from runtime.vm.instructions import Instruction, OpCode
from runtime.values.number import NumberValue
from runtime.values.string import StringValue

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
