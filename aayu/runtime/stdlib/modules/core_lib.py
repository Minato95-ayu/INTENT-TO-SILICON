"""
=============================================================================
FILE: core_lib.py
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
from ...values.string import StringValue
from ...values.null import NullValue

def register_core_lib(registry: StdLibRegistry):
    def fn_print(args, vm):
        val = args[0].stringify() if args and hasattr(args[0], "stringify") else str(args[0]) if args else ""
        print(val)
        vm.output.append(val)
        return NullValue()
    registry.register("core::print", fn_print)
    registry.register("print", fn_print)
    
    def fn_input(args, vm):
        prompt = args[0].stringify() if args else ""
        val = input(prompt)
        return make_string(vm, val)
    registry.register("core::input", fn_input)
    
    def fn_typeof(args, vm):
        if not args: return NullValue()
        return make_string(vm, args[0].type_name()) if hasattr(args[0], 'type_name') else str(type(args[0]).__name__)
    registry.register("core::typeof", fn_typeof)
    
    def fn_float(args, vm):
        if not args: return 0.0
        val = args[0]
        if hasattr(val, "value"): val = val.value
        try: return float(val)
        except (ValueError, TypeError): return 0.0
    registry.register("float", fn_float)
    
    def fn_int(args, vm):
        if not args: return 0
        val = args[0]
        if hasattr(val, "value"): val = val.value
        try: return int(float(val))
        except (ValueError, TypeError): return 0
    registry.register("int", fn_int)
