"""
=============================================================================
FILE: collections_ops.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ir import Opcode
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.string import StringValue

def handle_make_list(vm, frame, arg):
    elements = []
    for _ in range(arg):
        elements.insert(0, frame.stack.pop())
    obj = vm.memory.heap.allocate("list", elements)
    list_val = ListValue(obj.id, vm.memory.heap)
    frame.stack.append(list_val)

def handle_make_map(vm, frame, arg):
    temp = []
    for _ in range(arg):
        v = frame.stack.pop()
        k = frame.stack.pop()
        temp.insert(0, (k, v))
        
    elements = {}
    for k, v in temp:
        key_str = k.stringify()
        elements[key_str] = v
        
    obj = vm.memory.heap.allocate("map", elements)
    map_val = MapValue(obj.id, vm.memory.heap)
    frame.stack.append(map_val)
