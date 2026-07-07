"""
===============================================================================
AAYU Compiler - Memory Manager (DARC)

Purpose:
    Variables aur Objects kahan save honge aur kab delete honge, ye file manage karti hai. (Deterministic ARC)

Pipeline:
    Virtual Machine (VM)
        ↓
    Memory Manager ← (Current File)

Ye file kyun important hai?
    Agar memory delete nahi hui to Memory Leak ho jayega (RAM full). Ye ref-counting use karta hai object clean karne ke liye.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    8. runtime/stdlib/stdlib.py
    9. runtime/memory/manager.py (You are here)
    10. workspace/workspace.py
===============================================================================
"""
from typing import Dict, List, Any
from ..values.base import RuntimeValue
from ..values.null import NullValue
from .heap import Heap

class MemoryManager:
    def __init__(self):
        self.globals: Dict[str, RuntimeValue] = {}
        self.locals_stack: List[Dict[str, RuntimeValue]] = []
        self.constants: List[RuntimeValue] = []
        self.constants_stack: List[List[RuntimeValue]] = []
        self.heap = Heap()
        self.modules: Dict[str, RuntimeValue] = {}
        self.builtins: Dict[str, RuntimeValue] = {}

    def load(self, name: str) -> RuntimeValue:
        if self.locals_stack:
            current_locals = self.locals_stack[-1]
            if name in current_locals: return current_locals[name]
            
            # Check script-level locals (globals for the current script)
            if len(self.locals_stack) > 1:
                script_locals = self.locals_stack[0]
                if name in script_locals: return script_locals[name]
                
        if name in self.globals: return self.globals[name]
        if name in self.builtins: return self.builtins[name]
        return NullValue()

    def store(self, name: str, value: RuntimeValue):
        if self.locals_stack: self.locals_stack[-1][name] = value
        else: self.globals[name] = value

    def push_frame(self, initial_locals: Dict[str, RuntimeValue] = None):
        self.locals_stack.append(initial_locals if initial_locals is not None else {})

    def pop_frame(self):
        if self.locals_stack: self.locals_stack.pop()

    def get_locals(self) -> Dict[str, RuntimeValue]:
        if self.locals_stack: return self.locals_stack[-1]
        return self.globals

    def set_constants(self, constants_list: List[Any]):
        self.constants_stack.append(self.constants)
        self.constants = []
        from ..values.number import NumberValue
        from ..values.string import StringValue
        from ..values.boolean import BooleanValue
        from ..values.null import NullValue
        from ..values.function import FunctionValue
        from compiler.frontend.ir import Bytecode
        for raw_val in constants_list:
            if isinstance(raw_val, bool):
                self.constants.append(BooleanValue(raw_val))
            elif isinstance(raw_val, (int, float)):
                self.constants.append(NumberValue(raw_val))
            elif isinstance(raw_val, str):
                obj = self.heap.allocate("string", raw_val)
                self.constants.append(StringValue(obj.id, self.heap))
            elif isinstance(raw_val, Bytecode):
                self.constants.append(FunctionValue(raw_val.name, raw_val))
            elif raw_val is None:
                self.constants.append(NullValue())
            else:
                self.constants.append(raw_val)

    def restore_constants(self):
        if self.constants_stack:
            self.constants = self.constants_stack.pop()

    def load_constant(self, index: int) -> RuntimeValue:
        if 0 <= index < len(self.constants): return self.constants[index]
        return NullValue()
