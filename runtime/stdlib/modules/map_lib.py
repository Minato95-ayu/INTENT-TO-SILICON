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
    registry.register("map::keys", lambda args, vm: ListValue(vm.heap.allocate("list", [StringValue(vm.heap.allocate("string", k).id, vm.heap) for k in args[0]._get_payload().keys()]).id, vm.heap))
    registry.register("map::values", lambda args, vm: ListValue(vm.heap.allocate("list", list(args[0]._get_payload().values())).id, vm.heap))

