from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from aayu.compiler.machine_lir.nodes import MachineFunction, MachineInstruction, MachineOperand, OperandType
from aayu.runtime.vm.instructions import Opcode

@dataclass
class StackInstruction:
    opcode: int
    arg: Any = None
    label: str = None  # To mark block labels

class BytecodeLowering:
    def __init__(self):
        self.local_map: Dict[str, int] = {}
        self.next_local = 0
        self.instructions: List[StackInstruction] = []
        self.max_stack = 0
        self.current_stack = 0
        
    def _alloc_local(self, reg_name: str) -> int:
        if reg_name not in self.local_map:
            self.local_map[reg_name] = self.next_local
            self.next_local += 1
        return self.local_map[reg_name]
        
    def _get_local(self, reg_name: str) -> int:
        if reg_name not in self.local_map:
            return self._alloc_local(reg_name)
        return self.local_map[reg_name]
        
    def _push(self):
        self.current_stack += 1
        if self.current_stack > self.max_stack:
            self.max_stack = self.current_stack
            
    def _pop(self, count: int = 1):
        self.current_stack -= count
        if self.current_stack < 0:
            self.current_stack = 0
            
    def emit(self, opcode: int, arg: Any = None):
        self.instructions.append(StackInstruction(opcode=opcode, arg=arg))
        
        if opcode in (Opcode.PUSH_CONST, Opcode.LOAD_LOCAL, Opcode.LOAD_GLOBAL, Opcode.DUP):
            self._push()
        elif opcode in (Opcode.POP, Opcode.STORE_LOCAL, Opcode.STORE_GLOBAL, Opcode.JMP_IF_FALSE):
            self._pop()
        elif opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, 
                        Opcode.CMP_EQ, Opcode.CMP_NEQ, Opcode.CMP_LT, Opcode.CMP_GT, 
                        Opcode.CMP_LTE, Opcode.CMP_GTE):
            self._pop(2)
            self._push()
            
    def emit_label(self, name: str):
        self.instructions.append(StackInstruction(opcode=-1, label=name))
        
    def lower(self, func: MachineFunction) -> Tuple[List[StackInstruction], int, int]:
        for block in func.blocks:
            self.emit_label(str(block.name))
            
            for instr in block.instructions:
                op = instr.opcode
                
                if op == "LOAD_CONST":
                    self.emit(Opcode.PUSH_CONST, instr.operands[0].value)
                    if instr.dest:
                        dest_slot = self._alloc_local(str(instr.dest.value))
                        self.emit(Opcode.STORE_LOCAL, dest_slot)
                        
                elif op in ("ADD", "SUB", "MUL", "DIV", "CMP_EQ", "CMP_GT", "CMP_LT"):
                    for operand in instr.operands:
                        slot = self._get_local(str(operand.value))
                        self.emit(Opcode.LOAD_LOCAL, slot)
                        
                    vm_op = {
                        "ADD": Opcode.ADD,
                        "SUB": Opcode.SUB,
                        "MUL": Opcode.MUL,
                        "DIV": Opcode.DIV,
                        "CMP_EQ": Opcode.CMP_EQ,
                        "CMP_GT": Opcode.CMP_GT,
                        "CMP_LT": Opcode.CMP_LT,
                    }[op]
                    self.emit(vm_op)
                    
                    if instr.dest:
                        dest_slot = self._alloc_local(str(instr.dest.value))
                        self.emit(Opcode.STORE_LOCAL, dest_slot)
                        
                elif op == "MOVE":
                    src_slot = self._get_local(str(instr.operands[0].value))
                    self.emit(Opcode.LOAD_LOCAL, src_slot)
                    dest_slot = self._alloc_local(str(instr.dest.value))
                    self.emit(Opcode.STORE_LOCAL, dest_slot)
                    
                elif op == "JMP":
                    target_block = instr.operands[0].value
                    self.emit(Opcode.JMP, target_block)
                    
                elif op == "BRANCH":
                    cond_slot = self._get_local(str(instr.operands[0].value))
                    true_block = instr.operands[1].value
                    false_block = instr.operands[2].value
                    
                    self.emit(Opcode.LOAD_LOCAL, cond_slot)
                    self.emit(Opcode.JMP_IF_FALSE, false_block)
                    self.emit(Opcode.JMP, true_block)
                    
                elif op == "RET":
                    if instr.operands:
                        src_slot = self._get_local(str(instr.operands[0].value))
                        self.emit(Opcode.LOAD_LOCAL, src_slot)
                    else:
                        self.emit(Opcode.PUSH_CONST, None)
                    self.emit(Opcode.RET)
                    
                else:
                    raise NotImplementedError(f"Bytecode Lowering for {op} not implemented")
                    
        return self.instructions, self.next_local, self.max_stack + 2
