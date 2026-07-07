"""
=============================================================================
FILE: random_lib.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.null import NullValue
import random

def register_random_lib(registry: StdLibRegistry):
    def fn_int(args, vm):
        if len(args) < 2: return NullValue()
        return NumberValue(random.randint(int(args[0].to_python()), int(args[1].to_python())))
    registry.register("random::int", fn_int)
    
    def fn_float(args, vm):
        return NumberValue(random.random())
    registry.register("random::float", fn_float)
    
    def fn_choice(args, vm):
        if not args: return NullValue()
        elements = args[0].elements
        if not elements: return NullValue()
        return random.choice(elements)
    registry.register("random::choice", fn_choice)
