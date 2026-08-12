from typing import List
from aayu.runtime.vm.instructions import Opcode
from aayu.compiler.backend.bytecode.lowering import StackInstruction

class PeepholeOptimizer:
    def optimize(self, instructions: List[StackInstruction]) -> List[StackInstruction]:
        optimized = []
        i = 0
        n = len(instructions)
        
        while i < n:
            instr = instructions[i]
            
            # Rule 1: LOAD_LOCAL x; STORE_LOCAL x -> remove
            if i + 1 < n:
                next_instr = instructions[i + 1]
                if instr.opcode == Opcode.LOAD_LOCAL and next_instr.opcode == Opcode.STORE_LOCAL:
                    if instr.arg == next_instr.arg:
                        i += 2
                        continue
                        
            # Rule 2: LOAD_CONST a; LOAD_CONST b; ADD -> LOAD_CONST (a+b)
            if i + 2 < n:
                instr2 = instructions[i + 1]
                instr3 = instructions[i + 2]
                if (instr.opcode == Opcode.PUSH_CONST and 
                    instr2.opcode == Opcode.PUSH_CONST and 
                    instr3.opcode == Opcode.ADD):
                    
                    # Assuming args are the actual values, not constant pool indices yet
                    # because constant pool is built during emit phase
                    if isinstance(instr.arg, (int, float)) and isinstance(instr2.arg, (int, float)):
                        new_val = instr.arg + instr2.arg
                        optimized.append(StackInstruction(opcode=Opcode.PUSH_CONST, arg=new_val))
                        i += 3
                        continue
                        
            # Otherwise, keep instruction
            optimized.append(instr)
            i += 1
            
        return optimized
