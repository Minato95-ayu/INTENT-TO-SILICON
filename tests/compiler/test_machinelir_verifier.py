import pytest
from aayu.compiler.errors import DiagnosticEngine
from aayu.compiler.machine_lir.nodes import (
    MachineFunction, MachineBasicBlock, MachineInstruction,
    MachineOperand, OperandType, MachineRegister, RegisterClass
)
from aayu.compiler.machine_lir.verifier import MachineLIRVerifier

def test_machinelir_verifier_success():
    diag = DiagnosticEngine()
    verifier = MachineLIRVerifier(diag)
    
    func = MachineFunction("test")
    block = MachineBasicBlock("entry")
    
    r1 = MachineOperand(OperandType.REGISTER, MachineRegister(1, RegisterClass.GENERAL))
    r2 = MachineOperand(OperandType.REGISTER, MachineRegister(2, RegisterClass.GENERAL))
    
    instr = MachineInstruction("ADD", [r1, r2], r1)
    ret = MachineInstruction("RET", [])
    
    block.instructions = [instr, ret]
    func.blocks.append(block)
    func.entry_block = block
    
    assert verifier._verify_function(func) is None
    assert verifier.valid is True

def test_machinelir_verifier_missing_terminator():
    diag = DiagnosticEngine()
    verifier = MachineLIRVerifier(diag)
    
    func = MachineFunction("test")
    block = MachineBasicBlock("entry")
    
    r1 = MachineOperand(OperandType.REGISTER, MachineRegister(1, RegisterClass.GENERAL))
    r2 = MachineOperand(OperandType.REGISTER, MachineRegister(2, RegisterClass.GENERAL))
    
    instr = MachineInstruction("ADD", [r1, r2], r1)
    
    block.instructions = [instr] # No terminator
    func.blocks.append(block)
    func.entry_block = block
    
    verifier._verify_function(func)
    assert verifier.valid is False
    assert len(diag.diagnostics) > 0
    assert "does not end with a terminator" in diag.diagnostics[0].message
