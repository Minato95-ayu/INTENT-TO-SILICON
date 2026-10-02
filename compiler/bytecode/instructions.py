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

from dataclasses import dataclass
from typing import Any, List

@dataclass
class Instruction:
    opcode: str
    arg1: Any = None
    arg2: Any = None
    
    def serialize(self):
        return (self.opcode, self.arg1, self.arg2)

@dataclass
class BytecodeObject:
    instructions: List[Instruction]
    constants: List[Any]
