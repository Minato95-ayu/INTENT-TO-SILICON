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

import math

def register_math_lib(registry: StdLibRegistry):
    def fn_sin(args, vm):
        return NumberValue(math.sin(args[0].to_python()))
    def fn_cos(args, vm):
        return NumberValue(math.cos(args[0].to_python()))
    def fn_tan(args, vm):
        return NumberValue(math.tan(args[0].to_python()))
    def fn_sqrt(args, vm):
        return NumberValue(math.sqrt(args[0].to_python()))
    def fn_pow(args, vm):
        return NumberValue(math.pow(args[0].to_python(), args[1].to_python()))
    def fn_abs(args, vm):
        return NumberValue(abs(args[0].to_python()))
    def fn_round(args, vm):
        return NumberValue(round(args[0].to_python()))
        
    registry.register("math::sin", fn_sin)
    registry.register("math::cos", fn_cos)
    registry.register("math::tan", fn_tan)
    registry.register("math::sqrt", fn_sqrt)
    registry.register("math::pow", fn_pow)
    registry.register("math::abs", fn_abs)
    registry.register("math::round", fn_round)
