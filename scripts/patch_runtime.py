"""
=============================================================================
FILE: patch_runtime.py
PURPOSE: Patches runtime system
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles patches runtime system.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import shutil

runtime_dir = r"prototype\language\runtime"
values_dir = os.path.join(runtime_dir, "values")
memory_dir = os.path.join(runtime_dir, "memory")
vm_dir = os.path.join(runtime_dir, "vm")
stdlib_dir = os.path.join(runtime_dir, "stdlib")
gc_dir = os.path.join(runtime_dir, "gc")

os.makedirs(values_dir, exist_ok=True)
os.makedirs(memory_dir, exist_ok=True)
os.makedirs(vm_dir, exist_ok=True)
os.makedirs(stdlib_dir, exist_ok=True)
os.makedirs(gc_dir, exist_ok=True)

# 1. Values Split
base_val = """from abc import ABC, abstractmethod
from typing import Any

class RuntimeValue(ABC):
    @abstractmethod
    def type_name(self) -> str:
        pass

    @abstractmethod
    def truthy(self) -> bool:
        pass

    @abstractmethod
    def equals(self, other: 'RuntimeValue') -> bool:
        pass

    @abstractmethod
    def compare(self, other: 'RuntimeValue') -> int:
        pass

    @abstractmethod
    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot add {other.type_name()} to {self.type_name()}")
        
    @abstractmethod
    def sub(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot subtract {other.type_name()} from {self.type_name()}")
        
    @abstractmethod
    def mul(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot multiply {self.type_name()} by {other.type_name()}")
        
    @abstractmethod
    def div(self, other: 'RuntimeValue') -> 'RuntimeValue':
        raise Exception(f"Cannot divide {self.type_name()} by {other.type_name()}")

    @abstractmethod
    def clone(self) -> 'RuntimeValue':
        pass

    @abstractmethod
    def stringify(self) -> str:
        pass

    @abstractmethod
    def to_python(self) -> Any:
        pass
"""
with open(os.path.join(values_dir, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("from .base import RuntimeValue\nfrom .number import NumberValue\nfrom .string import StringValue\nfrom .boolean import BooleanValue\nfrom .null import NullValue\nfrom .list import ListValue\nfrom .map import MapValue\nfrom .function import FunctionValue, NativeFunctionValue\nfrom .module import ModuleValue\n")

with open(os.path.join(values_dir, "base.py"), "w", encoding="utf-8") as f:
    f.write(base_val)

# Null
null_val = """from .base import RuntimeValue
from typing import Any

class NullValue(RuntimeValue):
    def type_name(self) -> str: return "Null"
    def truthy(self) -> bool: return False
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, NullValue)
    def compare(self, other: RuntimeValue) -> int: return 0 if isinstance(other, NullValue) else -1
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return NullValue()
    def stringify(self) -> str: return "null"
    def to_python(self) -> Any: return None
"""
with open(os.path.join(values_dir, "null.py"), "w", encoding="utf-8") as f:
    f.write(null_val)

# Number
number_val = """from .base import RuntimeValue
from .boolean import BooleanValue
from typing import Any

class NumberValue(RuntimeValue):
    def __init__(self, value: float): self.value = float(value)
    def type_name(self) -> str: return "Number"
    def truthy(self) -> bool: return self.value != 0.0
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, NumberValue) and self.value == other.value
    def compare(self, other: RuntimeValue) -> int:
        if not isinstance(other, NumberValue): raise Exception("Cannot compare")
        if self.value < other.value: return -1
        if self.value > other.value: return 1
        return 0
    def add(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value + other.value)
        return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value - other.value)
        return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value * other.value)
        return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue):
            if other.value == 0: raise Exception("Division by zero")
            return NumberValue(self.value / other.value)
        return super().div(other)
    def clone(self) -> RuntimeValue: return NumberValue(self.value)
    def stringify(self) -> str: return str(int(self.value)) if self.value.is_integer() else str(self.value)
    def to_python(self) -> Any: return self.value
"""
with open(os.path.join(values_dir, "number.py"), "w", encoding="utf-8") as f:
    f.write(number_val)

# Boolean
boolean_val = """from .base import RuntimeValue
from typing import Any

class BooleanValue(RuntimeValue):
    def __init__(self, value: bool): self.value = bool(value)
    def type_name(self) -> str: return "Boolean"
    def truthy(self) -> bool: return self.value
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, BooleanValue) and self.value == other.value
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare boolean")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return BooleanValue(self.value)
    def stringify(self) -> str: return "true" if self.value else "false"
    def to_python(self) -> Any: return self.value
"""
with open(os.path.join(values_dir, "boolean.py"), "w", encoding="utf-8") as f:
    f.write(boolean_val)

# String
string_val = """from .base import RuntimeValue
from typing import Any

class StringValue(RuntimeValue):
    def __init__(self, value: str): self.value = value
    def type_name(self) -> str: return "String"
    def truthy(self) -> bool: return len(self.value) > 0
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, StringValue) and self.value == other.value
    def compare(self, other: RuntimeValue) -> int:
        if not isinstance(other, StringValue): raise Exception("Cannot compare")
        if self.value < other.value: return -1
        if self.value > other.value: return 1
        return 0
    def add(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, StringValue): return StringValue(self.value + other.value)
        return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return StringValue(self.value)
    def stringify(self) -> str: return self.value
    def to_python(self) -> Any: return self.value
"""
with open(os.path.join(values_dir, "string.py"), "w", encoding="utf-8") as f:
    f.write(string_val)

# List
list_val = """from .base import RuntimeValue
from typing import Any, List

class ListValue(RuntimeValue):
    def __init__(self, elements: List[RuntimeValue] = None): self.elements = elements if elements is not None else []
    def type_name(self) -> str: return "List"
    def truthy(self) -> bool: return len(self.elements) > 0
    def equals(self, other: RuntimeValue) -> bool:
        if not isinstance(other, ListValue) or len(self.elements) != len(other.elements): return False
        for a, b in zip(self.elements, other.elements):
            if not a.equals(b): return False
        return True
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare list")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return ListValue([e.clone() for e in self.elements])
    def stringify(self) -> str: return f"[{', '.join([e.stringify() for e in self.elements])}]"
    def to_python(self) -> Any: return [e.to_python() for e in self.elements]
"""
with open(os.path.join(values_dir, "list.py"), "w", encoding="utf-8") as f:
    f.write(list_val)

# Map
map_val = """from .base import RuntimeValue
from .null import NullValue
from typing import Any, Dict

class MapValue(RuntimeValue):
    def __init__(self, properties: Dict[str, RuntimeValue] = None): self.properties = properties if properties is not None else {}
    def type_name(self) -> str: return "Map"
    def truthy(self) -> bool: return len(self.properties) > 0
    def equals(self, other: RuntimeValue) -> bool:
        if not isinstance(other, MapValue) or len(self.properties) != len(other.properties): return False
        for k, v in self.properties.items():
            if k not in other.properties or not v.equals(other.properties[k]): return False
        return True
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare map")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return MapValue({k: v.clone() for k, v in self.properties.items()})
    def stringify(self) -> str: return f"{{{', '.join([f'{k}: {v.stringify()}' for k, v in self.properties.items()])}}}"
    def to_python(self) -> Any: return {k: v.to_python() for k, v in self.properties.items()}
"""
with open(os.path.join(values_dir, "map.py"), "w", encoding="utf-8") as f:
    f.write(map_val)

# Function
func_val = """from .base import RuntimeValue
from typing import Any

class FunctionValue(RuntimeValue):
    def __init__(self, name: str, bytecode: Any, env: Any = None):
        self.name = name; self.bytecode = bytecode; self.closure_env = env
    def type_name(self) -> str: return "Function"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare function")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<function {self.name}>"
    def to_python(self) -> Any: return self

class NativeFunctionValue(RuntimeValue):
    def __init__(self, name: str, call_fn: callable):
        self.name = name; self.call_fn = call_fn
    def type_name(self) -> str: return "NativeFunction"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare native function")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<native function {self.name}>"
    def to_python(self) -> Any: return self
"""
with open(os.path.join(values_dir, "function.py"), "w", encoding="utf-8") as f:
    f.write(func_val)

# Module
module_val = """from .base import RuntimeValue
from typing import Any, Dict

class ModuleValue(RuntimeValue):
    def __init__(self, name: str, exports: Dict[str, RuntimeValue] = None):
        self.name = name; self.exports = exports if exports is not None else {}
    def type_name(self) -> str: return "Module"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare module")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<module {self.name}>"
    def to_python(self) -> Any: return self
"""
with open(os.path.join(values_dir, "module.py"), "w", encoding="utf-8") as f:
    f.write(module_val)


# 2. Memory Split
with open(os.path.join(memory_dir, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("from .manager import MemoryManager\nfrom .heap import Heap\n")

heap_val = """from typing import Dict, Any
class Heap:
    def __init__(self):
        self.objects: Dict[int, Any] = {}
        self.next_address = 1
    def allocate(self, obj: Any) -> int:
        addr = self.next_address
        self.objects[addr] = obj
        self.next_address += 1
        return addr
    def free(self, address: int):
        if address in self.objects:
            del self.objects[address]
    def get(self, address: int) -> Any:
        return self.objects.get(address)
    def set(self, address: int, obj: Any):
        if address in self.objects:
            self.objects[address] = obj
"""
with open(os.path.join(memory_dir, "heap.py"), "w", encoding="utf-8") as f:
    f.write(heap_val)

manager_val = """from typing import Dict, List
from ..values import RuntimeValue, NullValue
from .heap import Heap

class MemoryManager:
    def __init__(self):
        self.globals: Dict[str, RuntimeValue] = {}
        self.locals_stack: List[Dict[str, RuntimeValue]] = []
        self.constants: List[RuntimeValue] = []
        self.heap = Heap()
        self.modules: Dict[str, RuntimeValue] = {}
        self.builtins: Dict[str, RuntimeValue] = {}

    def load(self, name: str) -> RuntimeValue:
        if self.locals_stack:
            current_locals = self.locals_stack[-1]
            if name in current_locals: return current_locals[name]
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

    def set_constants(self, constants_list: List[RuntimeValue]):
        self.constants = constants_list

    def load_constant(self, index: int) -> RuntimeValue:
        if 0 <= index < len(self.constants): return self.constants[index]
        return NullValue()
"""
with open(os.path.join(memory_dir, "manager.py"), "w", encoding="utf-8") as f:
    f.write(manager_val)

# Delete old files if they exist
old_values = os.path.join(runtime_dir, "values.py")
old_memory = os.path.join(runtime_dir, "memory.py")
if os.path.exists(old_values): os.remove(old_values)
if os.path.exists(old_memory): os.remove(old_memory)

# Move stdlib.py
old_stdlib = os.path.join(runtime_dir, "stdlib.py")
if os.path.exists(old_stdlib):
    shutil.move(old_stdlib, os.path.join(stdlib_dir, "stdlib.py"))
    # Create __init__.py for stdlib
    with open(os.path.join(stdlib_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("from .stdlib import StdLib\n")

print("Runtime refactored successfully.")
