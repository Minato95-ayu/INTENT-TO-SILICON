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

from .base import RuntimeValue

class StackValue(RuntimeValue):
    def __init__(self, elements=None):
        self.elements = elements if elements else []
        
    def type_name(self) -> str:
        return "Stack"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, StackValue): return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return StackValue(list(self.elements))
        
    def stringify(self) -> str:
        return f"Stack({self.elements})"
        
    def to_python(self):
        return self.elements
