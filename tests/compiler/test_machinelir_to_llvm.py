import pytest
from aayu.compiler.machine_lir.nodes import (
    MachineModule, MachineFunction, MachineBasicBlock, MachineInstruction,
    MachineOperand, OperandType, MachineRegister, RegisterClass
)
from aayu.compiler.backend.llvm.lowering import LLVMBackend

def test_machinelir_to_llvm_lowering():
    # 1. Construct simple MachineLIR program:
    # r1 = LOAD_CONST 10
    # r2 = LOAD_CONST 20
    # r3 = ADD r1, r2
    # RET r3
    
    module = MachineModule()
    func = MachineFunction("test_add")
    module.functions.append(func)
    
    block = MachineBasicBlock("entry")
    func.blocks.append(block)
    func.entry_block = block
    
    r1 = MachineOperand(OperandType.REGISTER, MachineRegister("r1", RegisterClass.GENERAL))
    r2 = MachineOperand(OperandType.REGISTER, MachineRegister("r2", RegisterClass.GENERAL))
    r3 = MachineOperand(OperandType.REGISTER, MachineRegister("r3", RegisterClass.GENERAL))
    
    c10 = MachineOperand(OperandType.IMMEDIATE, "10")
    c20 = MachineOperand(OperandType.IMMEDIATE, "20")
    
    i1 = MachineInstruction("LOAD_CONST", [c10], r1)
    i2 = MachineInstruction("LOAD_CONST", [c20], r2)
    i3 = MachineInstruction("ADD", [r1, r2], r3)
    i4 = MachineInstruction("RET", [r3])
    
    block.instructions = [i1, i2, i3, i4]
    
    # 2. Lower to LLVM IR
    backend = LLVMBackend()
    artifact = backend.lower(module)
    
    ll_bytes = artifact.generate()
    ll_string = ll_bytes.decode('utf-8')
    
    # 3. Verify string representation
    # Notice that constants are directly embedded into the ADD instruction
    # due to the logic in `lower_load_const`.
    expected = (
        "; ModuleID = 'aayu_module'\n"
        "source_filename = \"aayu_module\"\n\n"
        "define i32 @test_add() {\n"
        "entry:\n"
        "  %r3 = add i32 10, 20\n"
        "  ret i32 %r3\n"
        "}\n"
    )
    
    assert ll_string == expected
