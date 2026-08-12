import pytest
pytest.importorskip("llvmlite")

from aayu.compiler.lir.nodes import FunctionLIR, LIRInstruction, LIROpcode, LIRBlock
from aayu.compiler.mir.nodes import RegisterID
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.backend.llvm.lowering import LLVMBackend
from aayu.compiler.backend.llvm.bridge import LLVMBridge
from aayu.compiler.machine_lir.nodes import MachineModule

def run_interpreter(func_lir: FunctionLIR) -> int:
    regs = {}
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

def test_differential_lir_jit():
    r1 = RegisterID("r1")
    r2 = RegisterID("r2")
    r3 = RegisterID("r3")
    r4 = RegisterID("r4")
    r5 = RegisterID("r5")
    
    block = LIRBlock("entry")
    block.instructions = [
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [50], r1),
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [15], r2),
        LIRInstruction(LIROpcode.LIR_ADD, [r1, r2], r3),      # r3 = 65
        LIRInstruction(LIROpcode.LIR_LOAD_CONST, [5], r4),
        LIRInstruction(LIROpcode.LIR_SUB, [r3, r4], r5),      # r5 = 60
        LIRInstruction(LIROpcode.LIR_RET, [r5])
    ]
    
    func_lir = FunctionLIR("test_diff_jit")
    func_lir.blocks.append(block)
    
    # Run Interpreter
    interp_res = run_interpreter(func_lir)
    
    # Lower to MachineLIR
    machine_lowering = MachineLIRLowering()
    func_machine = machine_lowering.lower(func_lir)
    
    machine_mod = MachineModule()
    machine_mod.functions.append(func_machine)
    
    # Lower to LLVM
    llvm_backend = LLVMBackend()
    llvm_artifact = llvm_backend.lower(machine_mod)
    
    bridge = LLVMBridge()
    ll_mod = bridge.parse_module(llvm_artifact.llvm_module)
    
    bridge.verify(ll_mod)
    bridge.optimize(ll_mod, profile="ReleaseFast")
    
    bridge.create_jit(ll_mod)
    jit_res = bridge.run_function("test_diff_jit")
    
    assert jit_res == interp_res
    assert jit_res == 60
