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

from ..collections.list import list_append, list_length, list_get, list_set, list_remove, list_contains, list_pop, list_insert, list_reverse, list_sort

def register_list_lib(registry: StdLibRegistry):
    registry.register("list::push", list_append)
    registry.register("list::pop", list_pop)
    registry.register("list::shift", lambda args, vm: list_remove([args[0], NumberValue(0)], vm))
    registry.register("list::unshift", lambda args, vm: list_insert([args[0], NumberValue(0), args[1]], vm))
    registry.register("list::length", list_length)
    registry.register("list::get", list_get)
    registry.register("list::set", list_set)
    registry.register("list::remove", list_remove)
    registry.register("list::contains", list_contains)
    registry.register("list::insert", list_insert)
    registry.register("list::reverse", list_reverse)
    registry.register("list::sort", list_sort)
