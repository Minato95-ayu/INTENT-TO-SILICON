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
    obj_id = vm.heap.allocate("string", text)
    return StringValue(obj_id, vm.heap)

def make_list(vm, elements: list) -> ListValue:
    obj_id = vm.heap.allocate("list", elements)
    return ListValue(obj_id, vm.heap)

def make_map(vm, elements: dict) -> MapValue:
    obj_id = vm.heap.allocate("map", elements)
    return MapValue(obj_id, vm.heap)

