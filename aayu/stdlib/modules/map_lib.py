"""
=============================================================================
FILE: map_lib.py
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

from ..collections.map import map_set, map_get, map_length, map_remove, map_contains

def register_map_lib(registry: StdLibRegistry):
    registry.register("map::put", map_set)
    registry.register("map::get", map_get)
    registry.register("map::length", map_length)
    registry.register("map::remove", map_remove)
    registry.register("map::contains", map_contains)
    registry.register("map::keys", lambda args, vm: ListValue(vm.memory.heap.allocate("list", [StringValue(vm.memory.heap.allocate("string", k).id, vm.memory.heap) for k in args[0]._get_payload().keys()]).id, vm.memory.heap))
    registry.register("map::values", lambda args, vm: ListValue(vm.memory.heap.allocate("list", list(args[0]._get_payload().values())).id, vm.memory.heap))
