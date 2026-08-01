import unittest
import os
import json
import socket
from unittest.mock import patch, MagicMock

# AAYU Runtime Imports
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.stdlib.stdlib import StdLib
from aayu.runtime.values.string import StringValue
from aayu.runtime.values.number import NumberValue
from aayu.runtime.values.boolean import BooleanValue
from aayu.runtime.values.null import NullValue
from aayu.runtime.values.map import MapValue

vm = VirtualMachine()
loader = StdLib(vm)
vm._register_stdlib = lambda: None # mock as it's already registered via loader

def _py_to_val(val):
    if isinstance(val, str):
        obj = vm.memory.heap.allocate("string", val)
        return StringValue(obj.id, vm.memory.heap)
    if isinstance(val, (int, float)):
        return NumberValue(val)
    return NullValue()

def execute(method, *args):
    return loader.registry.call(method, [_py_to_val(a) for a in args], vm)

unicode_str = '{"lang": "हिंदी"}'
parsed = execute("json::parse", unicode_str)
print("Parsed type:", type(parsed))
if isinstance(parsed, MapValue):
    print("Parsed dict:", parsed.to_python())
elif isinstance(parsed, StringValue):
    print("Parsed Error string:", parsed.to_python())

stringified = execute("json::stringify", parsed)
print("Stringified type:", type(stringified))
if hasattr(stringified, "to_python"):
    print("Stringified:", stringified.to_python())
