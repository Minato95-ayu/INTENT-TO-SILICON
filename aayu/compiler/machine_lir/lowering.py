from typing import Dict, Any, List
from aayu.compiler.lir.nodes import FunctionLIR, LIRBlock, LIRInstruction, LIROpcode
from aayu.compiler.machine_lir.nodes import (
    MachineModule, MachineFunction, MachineBasicBlock, MachineInstruction,
    MachineRegister, RegisterClass, MachineOperand, OperandType
)
from aayu.compiler.mir.nodes import RegisterID

class MachineLIRLowering:
    """
    Lowers target-agnostic LIR into physical-aware MachineLIR.
    """
    def __init__(self):
        self.block_map: Dict[str, MachineBasicBlock] = {}
        
    def lower(self, func_lir: FunctionLIR) -> MachineFunction:
        m_func = MachineFunction(name=func_lir.name)
        self.block_map.clear()
        
        # 1. Create blocks
        for lir_block in func_lir.blocks:
            m_block = MachineBasicBlock(name=lir_block.name)
            self.block_map[lir_block.name] = m_block
            m_func.blocks.append(m_block)
            if func_lir.entry_block and lir_block.name == func_lir.entry_block.name:
                m_func.entry_block = m_block
                
        # 2. Map CFG Edges
        for lir_block in func_lir.blocks:
            m_block = self.block_map[lir_block.name]
            m_block.predecessors = [self.block_map[p.name] for p in lir_block.predecessors]
            m_block.successors = [self.block_map[s.name] for s in lir_block.successors]
            
        # 3. Translate Instructions
        for lir_block in func_lir.blocks:
            m_block = self.block_map[lir_block.name]
            for instr in lir_block.instructions:
                m_instr = self._lower_instruction(instr)
                m_block.instructions.append(m_instr)
                
        return m_func
        
    def _lower_instruction(self, instr: LIRInstruction) -> MachineInstruction:
        # Mapping LIR Opcode to generic string Opcode for MachineLIR
        op_map = {
            LIROpcode.LIR_LOAD_CONST: "LOAD_CONST",
            LIROpcode.LIR_LOAD_ENUM_CONST: "LOAD_ENUM_CONST",
            LIROpcode.LIR_LOAD_LOCAL: "LOAD_LOCAL",
            LIROpcode.LIR_LOAD_GLOBAL: "LOAD_GLOBAL",
            LIROpcode.LIR_LOAD_LOCAL_PTR: "LOAD_LOCAL_PTR",
            LIROpcode.LIR_LOAD_GLOBAL_PTR: "LOAD_GLOBAL_PTR",
            LIROpcode.LIR_STORE_LOCAL: "STORE_LOCAL",
            LIROpcode.LIR_STORE_GLOBAL: "STORE_GLOBAL",
            LIROpcode.LIR_MOVE: "MOVE",
            LIROpcode.LIR_ADD: "ADD",
            LIROpcode.LIR_SUB: "SUB",
            LIROpcode.LIR_MUL: "MUL",
            LIROpcode.LIR_DIV: "DIV",
            LIROpcode.LIR_AND: "AND",
            LIROpcode.LIR_CMP_EQ: "CMP_EQ",
            LIROpcode.LIR_CMP_GT: "CMP_GT",
            LIROpcode.LIR_CMP_LT: "CMP_LT",
            LIROpcode.LIR_JUMP: "JMP",
            LIROpcode.LIR_BRANCH: "BRANCH",
            LIROpcode.LIR_CALL: "CALL",
            LIROpcode.LIR_RET: "RET",
            LIROpcode.LIR_ALLOC: "ALLOC",
            LIROpcode.LIR_GEP: "GEP",
            LIROpcode.LIR_LOAD: "LOAD",
            LIROpcode.LIR_STORE: "STORE",
        }
        
        m_opcode = op_map.get(instr.opcode, instr.opcode.name)
        
        # Convert Operands
        m_operands = []
        for op in instr.operands:
            if isinstance(op, RegisterID):
                # We assume virtual registers are GENERAL class for now.
                # In the future, we would analyze type info.
                reg_id = int(op.id.replace("v", "").replace("p", "").replace("r", "")) if isinstance(op.id, str) and (op.id.startswith('v') or op.id.startswith('p') or op.id.startswith('r')) else id(op)
                m_operands.append(MachineOperand(OperandType.REGISTER, MachineRegister(id=reg_id, reg_class=RegisterClass.GENERAL)))
            elif isinstance(op, LIRBlock):
                m_operands.append(MachineOperand(OperandType.LABEL, self.block_map[op.name].name))
            else:
                m_operands.append(MachineOperand(OperandType.IMMEDIATE, op))
                
        # Convert Dest
        m_dest = None
        if instr.dest:
            reg_id = int(instr.dest.id.replace("v", "").replace("p", "").replace("r", "")) if isinstance(instr.dest.id, str) and (instr.dest.id.startswith('v') or instr.dest.id.startswith('p') or instr.dest.id.startswith('r')) else id(instr.dest)
            m_dest = MachineOperand(OperandType.REGISTER, MachineRegister(id=reg_id, reg_class=RegisterClass.GENERAL))
            
        return MachineInstruction(
            opcode=m_opcode,
            operands=m_operands,
            dest=m_dest,
            span=instr.span
        )
