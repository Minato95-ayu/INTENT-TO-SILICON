"""
=============================================================================
FILE: list_lib.py
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

def register_list_lib(registry: StdLibRegistry):
    def fn_mock(args, vm):
        return StringValue("Mock implementation for list")
        
    # Register basic API methods
    for method in ['push', 'pop', 'shift', 'unshift', 'map', 'filter']:
        registry.register(f"list::{method}", fn_mock)
