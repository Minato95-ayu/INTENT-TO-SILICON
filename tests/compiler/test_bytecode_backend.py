import pytest
from aayu.compiler.lir.nodes import FunctionLIR, LIRInstruction, LIROpcode
from aayu.compiler.mir.nodes import BasicBlock, RegisterID
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.backend.bytecode.lowering import BytecodeLowering
from aayu.compiler.backend.bytecode.peephole import PeepholeOptimizer
from aayu.compiler.backend.bytecode.emitter import BytecodeEmitter
from aayu.compiler.backend.bytecode.verifier import BytecodeVerifier
from aayu.compiler.backend.bytecode.aybc import AYBCFile
from aayu.runtime.vm.vm import VirtualMachine

def test_bytecode_lowering_and_execution():
    # 1. Setup simple LIR:
    # r1 = LOAD_CONST 10
    # r2 = LOAD_CONST 20
    # r3 = ADD r1, r2
    # RET r3
    
    r1 = RegisterID("r1")
    r2 = RegisterID("r2")
    r3 = RegisterID("r3")
    
    block = BasicBlock(0, "entry")
    block.instructions = [
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [10], r1),
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [20], r2),
        LIRInstruction(LIROpcode.LIR_ADD, [r1, r2], r3),
        LIRInstruction(LIROpcode.LIR_RET, [r3])
    ]
    
    # We must mock an LIR block here since FunctionLIR expects LIRBlock
    from aayu.compiler.lir.nodes import LIRBlock
    lir_block = LIRBlock(name="entry")
    lir_block.instructions = block.instructions
    
    func_lir = FunctionLIR("test_func")
    func_lir.blocks.append(lir_block)
    
    # 2. Lower to MachineLIR
    machine_lowering = MachineLIRLowering()
    func_machine = machine_lowering.lower(func_lir)
    
    # 3. Lower MachineLIR to Stack Instructions
    lowering = BytecodeLowering()
    instructions, locals_count, max_stack = lowering.lower(func_machine)
    
    assert len(instructions) > 0
    
    # 4. Peephole
    optimizer = PeepholeOptimizer()
    optimized = optimizer.optimize(instructions)
    
    # 5. Emitter
    emitter = BytecodeEmitter()
    emitter.emit_function("test_func", optimized, locals_count, max_stack)
    
    binary = emitter.generate()
    
    # 6. Verifier
    verifier = BytecodeVerifier(emitter.aybc)
    assert verifier.verify() is True
    
    # 7. VM Integration
    vm = VirtualMachine()
    vm.load_aybc(binary)
    
    assert "test_func" in vm.action_addresses
    
    # Execute the function
    vm.call_action_by_name("test_func")
    
    # Check the result (returned value should be on top of value_stack)
    assert vm.value_stack.depth() == 1
    assert vm.value_stack.pop() == 30

