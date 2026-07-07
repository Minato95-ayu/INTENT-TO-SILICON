"""
=============================================================================
FILE: math_lib.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
"""
from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.number import NumberValue
from ...values.boolean import BooleanValue

def register_math_lib(registry: StdLibRegistry):
    def fn_mock(args, vm):
        return StringValue("Mock implementation for math")
        
    # Register basic API methods
    for method in ['sin', 'cos', 'tan', 'sqrt', 'pow', 'abs', 'round']:
        registry.register(f"math::{method}", fn_mock)
