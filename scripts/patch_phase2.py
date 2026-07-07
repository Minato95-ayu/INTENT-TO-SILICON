"""
=============================================================================
FILE: patch_phase2.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import re

# 1. Update values.py
values_path = r"prototype\aayu_language\runtime\values.py"
with open(values_path, "r", encoding="utf-8") as f:
    v_content = f.read()

# Replace copy with clone
v_content = v_content.replace("def copy(", "def clone(")
v_content = v_content.replace(".copy()", ".clone()")

# Add default operator methods to RuntimeValue
default_methods = """
    @abstractmethod
    def to_python(self) -> Any:
        pass

    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot add {other.type_name()} to {self.type_name()}")
        
    def sub(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot subtract {other.type_name()} from {self.type_name()}")
        
    def mul(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot multiply {self.type_name()} by {other.type_name()}")
        
    def div(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot divide {self.type_name()} by {other.type_name()}")
        
    def mod(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot modulo {self.type_name()} by {other.type_name()}")

    def less_than(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot compare {self.type_name()} < {other.type_name()}")

    def greater_than(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot compare {self.type_name()} > {other.type_name()}")

    def less_than_or_equal(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot compare {self.type_name()} <= {other.type_name()}")

    def greater_than_or_equal(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot compare {self.type_name()} >= {other.type_name()}")
"""

if "def to_python" not in v_content:
    v_content = v_content.replace("def to_string(self) -> str:\n        pass", "def to_string(self) -> str:\n        pass\n" + default_methods)

# NullValue to_python
v_content = v_content.replace('def to_string(self) -> str:\n        return "null"', 'def to_string(self) -> str:\n        return "null"\n\n    def to_python(self) -> Any:\n        return None')

# BooleanValue to_python
v_content = v_content.replace('def to_string(self) -> str:\n        return "true" if self.value else "false"', 'def to_string(self) -> str:\n        return "true" if self.value else "false"\n\n    def to_python(self) -> Any:\n        return self.value')

# NumberValue to_python & ops
num_ops = """
    def to_python(self) -> Any:
        return self.value
        
    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return NumberValue(self.value + other.value)
        return super().add(other)
        
    def sub(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return NumberValue(self.value - other.value)
        return super().sub(other)
        
    def mul(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return NumberValue(self.value * other.value)
        return super().mul(other)
        
    def div(self, other: 'RuntimeValue') -> 'RuntimeValue':
        from .errors import DivisionByZeroError if False else Exception
        if isinstance(other, NumberValue):
            if other.value == 0: raise Exception("Division by zero")
            return NumberValue(self.value / other.value)
        return super().div(other)
        
    def mod(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue):
            if other.value == 0: raise Exception("Modulo by zero")
            return NumberValue(self.value % other.value)
        return super().mod(other)
        
    def less_than(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return BooleanValue(self.value < other.value)
        return super().less_than(other)
        
    def greater_than(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return BooleanValue(self.value > other.value)
        return super().greater_than(other)
        
    def less_than_or_equal(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return BooleanValue(self.value <= other.value)
        return super().less_than_or_equal(other)
        
    def greater_than_or_equal(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, NumberValue): return BooleanValue(self.value >= other.value)
        return super().greater_than_or_equal(other)
"""
if "def add(self, other:" not in v_content.split("class NumberValue")[1].split("class StringValue")[0]:
    v_content = v_content.replace('def to_string(self) -> str:\n        if self.value.is_integer():\n            return str(int(self.value))\n        return str(self.value)', 'def to_string(self) -> str:\n        if self.value.is_integer():\n            return str(int(self.value))\n        return str(self.value)\n' + num_ops)

# StringValue to_python & ops
str_ops = """
    def to_python(self) -> Any:
        return self.value
        
    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, StringValue): return StringValue(self.value + other.value)
        return super().add(other)
"""
if "def to_python" not in v_content.split("class StringValue")[1].split("class BooleanValue")[0]:
    v_content = v_content.replace('def to_string(self) -> str:\n        return self.value', 'def to_string(self) -> str:\n        return self.value\n' + str_ops)

# ListValue, MapValue, FunctionValue, NativeFunctionValue, ModuleValue to_python
for cls_name in ["ListValue", "MapValue", "FunctionValue", "NativeFunctionValue", "ModuleValue"]:
    part_start = v_content.split(f"class {cls_name}")[1]
    if "def to_python" not in part_start:
        if cls_name == "ListValue":
            v_content = v_content.replace('return len(self.elements)', 'return len(self.elements)\n\n    def to_python(self) -> Any:\n        return [e.to_python() for e in self.elements]')
        elif cls_name == "MapValue":
            v_content = v_content.replace('return self.properties.get(key, NullValue())', 'return self.properties.get(key, NullValue())\n\n    def to_python(self) -> Any:\n        return {k: v.to_python() for k, v in self.properties.items()}')
        else:
            to_str = f"class {cls_name}(RuntimeValue):"
            v_content = re.sub(r'(def to_string\(self\) -> str:\n\s+return [^\n]+)', r'\1\n\n    def to_python(self) -> Any:\n        return self', v_content, count=1, flags=re.DOTALL) # wait regex is risky.

# Let's just do simple replace for the rest
v_content = v_content.replace('return f"<function {self.name}>"', 'return f"<function {self.name}>"\n\n    def to_python(self) -> Any:\n        return self')
v_content = v_content.replace('return f"<native function {self.name}>"', 'return f"<native function {self.name}>"\n\n    def to_python(self) -> Any:\n        return self')
v_content = v_content.replace('return f"<module {self.name}>"', 'return f"<module {self.name}>"\n\n    def to_python(self) -> Any:\n        return self')

# Write values.py
with open(values_path, "w", encoding="utf-8") as f:
    f.write(v_content)
print("Updated values.py")

# 2. Update memory.py
mem_path = r"prototype\aayu_language\runtime\memory.py"
with open(mem_path, "r", encoding="utf-8") as f:
    m_content = f.read()
if "self.heap = {}" not in m_content:
    m_content = m_content.replace("self.constants: List[RuntimeValue] = []", "self.constants: List[RuntimeValue] = []\n        self.heap: Dict[int, Any] = {}")
    with open(mem_path, "w", encoding="utf-8") as f:
        f.write(m_content)
    print("Updated memory.py")
