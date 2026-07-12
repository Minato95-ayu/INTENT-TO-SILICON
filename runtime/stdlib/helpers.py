"""
=============================================================================
FILE: helpers.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ..values.string import StringValue
from ..values.list import ListValue
from ..values.map import MapValue

def make_string(vm, text: str) -> StringValue:
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def make_list(vm, elements: list) -> ListValue:
    obj = vm.memory.heap.allocate("list", elements)
    return ListValue(obj.id, vm.memory.heap)

def make_map(vm, elements: dict) -> MapValue:
    obj = vm.memory.heap.allocate("map", elements)
    return MapValue(obj.id, vm.memory.heap)
