from ...values.null import NullValue
from ...values.map import MapValue
from ...values.string import StringValue
from ...values.base import RuntimeValue

def map_set(args: list, vm) -> RuntimeValue:
    if len(args) < 3:
        raise Exception("map_set requires a map, a key, and a value")
    m = args[0]
    key = args[1]
    val = args[2]
    if not isinstance(m, MapValue):
        raise Exception(f"Expected a map, got {m.type_name()}")
    m.set(key, val)
    return NullValue()

def map_get(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("map_get requires a map and a key")
    m = args[0]
    key = args[1]
    if not isinstance(m, MapValue):
        raise Exception(f"Expected a map, got {m.type_name()}")
    return m.get(key)

def map_length(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("map_length requires a map")
    m = args[0]
    if not isinstance(m, MapValue):
        raise Exception(f"Expected a map, got {m.type_name()}")
    return m.length()

def map_remove(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("map_remove requires a map and a key")
    m = args[0]
    key = args[1]
    if not isinstance(m, MapValue):
        raise Exception(f"Expected a map, got {m.type_name()}")
    m.remove(key)
    return NullValue()

def map_contains(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("map_contains requires a map and a key")
    m = args[0]
    key = args[1]
    if not isinstance(m, MapValue):
        raise Exception(f"Expected a map, got {m.type_name()}")
    return m.contains(key)

def register_map_stdlib(registry):
    registry.register("map_set", map_set)
    registry.register("map_get", map_get)
    registry.register("map_length", map_length)
    registry.register("map_remove", map_remove)
    registry.register("map_contains", map_contains)
