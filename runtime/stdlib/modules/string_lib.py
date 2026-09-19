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
FILE: string_lib.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ..helpers import make_string, make_list, make_map
from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.boolean import BooleanValue
from ...values.null import NullValue
from ...values.list import ListValue

def get_val(arg):
    val = arg.to_python() if hasattr(arg, 'to_python') else arg
    if val is None: return ""
    return str(val)

def register_string_lib(registry: StdLibRegistry):
    def fn_split(args, vm):
        if len(args) < 2: return NullValue()
        parts = get_val(args[0]).split(get_val(args[1]))
        return make_list(vm, [make_string(vm, p) for p in parts])
    registry.register("string::split", fn_split)
    
    def fn_trim(args, vm):
        if not args: return NullValue()
        return make_string(vm, get_val(args[0]).strip())
    registry.register("string::trim", fn_trim)
    
    def fn_replace(args, vm):
        if len(args) < 3: return NullValue()
        return make_string(vm, get_val(args[0]).replace(get_val(args[1]), get_val(args[2])))
    registry.register("string::replace", fn_replace)
    
    def fn_upper(args, vm):
        if not args: return NullValue()
        return make_string(vm, get_val(args[0]).upper())
    registry.register("string::upper", fn_upper)
    
    def fn_lower(args, vm):
        if not args: return NullValue()
        return make_string(vm, get_val(args[0]).lower())
    registry.register("string::lower", fn_lower)
    
    def fn_contains(args, vm):
        if len(args) < 2: return False
        return bool(get_val(args[1]) in get_val(args[0]))
    registry.register("string::contains", fn_contains)
    
    def fn_starts_with(args, vm):
        if len(args) < 2: return False
        return bool(get_val(args[0]).startswith(get_val(args[1])))
    registry.register("string::starts_with", fn_starts_with)
    
    def fn_ends_with(args, vm):
        if len(args) < 2: return False
        return bool(get_val(args[0]).endswith(get_val(args[1])))
    registry.register("string::ends_with", fn_ends_with)

    def fn_length(args, vm):
        if not args: return 0
        return int(len(get_val(args[0])))
    registry.register("string::length", fn_length)
