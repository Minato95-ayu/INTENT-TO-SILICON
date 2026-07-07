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

def register_string_lib(registry: StdLibRegistry):
    def fn_split(args, vm):
        if len(args) < 2: return NullValue()
        parts = args[0].to_python().split(args[1].to_python())
        return make_list(vm, [make_string(vm, p) for p in parts])
    registry.register("string::split", fn_split)
    
    def fn_trim(args, vm):
        if not args: return NullValue()
        return make_string(vm, args[0].to_python().strip())
    registry.register("string::trim", fn_trim)
    
    def fn_replace(args, vm):
        if len(args) < 3: return NullValue()
        return make_string(vm, args[0].to_python().replace(args[1].to_python(), args[2].to_python()))
    registry.register("string::replace", fn_replace)
    
    def fn_upper(args, vm):
        if not args: return NullValue()
        return make_string(vm, args[0].to_python().upper())
    registry.register("string::upper", fn_upper)
    
    def fn_lower(args, vm):
        if not args: return NullValue()
        return make_string(vm, args[0].to_python().lower())
    registry.register("string::lower", fn_lower)
    
    def fn_contains(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[1].to_python() in args[0].to_python())
    registry.register("string::contains", fn_contains)
    
    def fn_starts_with(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[0].to_python().startswith(args[1].to_python()))
    registry.register("string::starts_with", fn_starts_with)
    
    def fn_ends_with(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[0].to_python().endswith(args[1].to_python()))
    registry.register("string::ends_with", fn_ends_with)

    def fn_length(args, vm):
        if not args: return NullValue()
        return NumberValue(len(args[0].to_python()))
    registry.register("string::length", fn_length)
