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

from typing import List
from compiler.ir.lir import LIRNode
from .instructions import Instruction, BytecodeObject

class BytecodeGenerator:
    def generate(self, lir: List[LIRNode]) -> BytecodeObject:
        instructions = []
        constants = []
        
        for node in lir:
            arg1 = node.operands[0] if len(node.operands) > 0 else None
            arg2 = node.operands[1] if len(node.operands) > 1 else None
            
            inst = Instruction(opcode=node.opcode, arg1=arg1, arg2=arg2)
            instructions.append(inst)
            
        return BytecodeObject(instructions=instructions, constants=constants)
