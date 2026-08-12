import pytest
from aayu.compiler.lir.nodes import FunctionLIR, LIRInstruction, LIROpcode
from aayu.compiler.mir.nodes import BasicBlock, RegisterID
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.backend.bytecode.lowering import BytecodeLowering
from aayu.compiler.backend.bytecode.peephole import PeepholeOptimizer
from aayu.compiler.backend.bytecode.emitter import BytecodeEmitter
from aayu.compiler.backend.bytecode.aybc import AYBCFile
from aayu.runtime.vm.vm import VirtualMachine
from aayu.compiler.lir.nodes import LIRBlock

def run_bytecode_vm(func_machine) -> int:
    lowering = BytecodeLowering()
    instructions, locals_count, max_stack = lowering.lower(func_machine)
    
    optimizer = PeepholeOptimizer()
    optimized = optimizer.optimize(instructions)
    
    emitter = BytecodeEmitter()
    emitter.emit_function(func_machine.name, optimized, locals_count, max_stack)
    binary = emitter.generate()
    
    vm = VirtualMachine()
    vm.load_aybc(binary)
    vm.call_action_by_name(func_machine.name)
    
    return vm.value_stack.pop()

def run_interpreter(func_lir: FunctionLIR) -> int:
    # A simple mock interpreter for the LIR level
    regs = {}
    
    # We just run linearly for this simple test
    for block in func_lir.blocks:
        for instr in block.instructions:
            if instr.opcode == LIROpcode.LIR_LOAD_CONST:
                regs[instr.dest.id] = instr.operands[0]
            elif instr.opcode == LIROpcode.LIR_ADD:
                regs[instr.dest.id] = regs[instr.operands[0].id] + regs[instr.operands[1].id]
            elif instr.opcode == LIROpcode.LIR_SUB:
                regs[instr.dest.id] = regs[instr.operands[0].id] - regs[instr.operands[1].id]
            elif instr.opcode == LIROpcode.LIR_RET:
                return regs[instr.operands[0].id]
    
    return 0

def test_differential_machinelir():
    """
    Validates that:
    MachineLIR -> Bytecode -> VM
    produces the exact same result as
    LIR -> Interpreter
    """
    # 1. Setup simple LIR
    r1 = RegisterID("r1")
    r2 = RegisterID("r2")
    r3 = RegisterID("r3")
    r4 = RegisterID("r4")
    
    block = LIRBlock("entry")
    block.instructions = [
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [50], r1),
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [15], r2),
        LIRInstruction(LIROpcode.LIR_ADD, [r1, r2], r3),      # r3 = 65
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [5], r4),
        LIRInstruction(LIROpcode.LIR_SUB, [r3, r4], r1),      # r1 = 60
        LIRInstruction(LIROpcode.LIR_RET, [r1])
    ]
    
    func_lir = FunctionLIR("test_diff")
    func_lir.blocks.append(block)
    
    # 2. Lower to MachineLIR
    machine_lowering = MachineLIRLowering()
    func_machine = machine_lowering.lower(func_lir)
    
    # 3. Get results
    vm_result = run_bytecode_vm(func_machine)
    interpreter_result = run_interpreter(func_lir)
    
    # 4. Compare
    assert vm_result == interpreter_result
    assert vm_result == 60
