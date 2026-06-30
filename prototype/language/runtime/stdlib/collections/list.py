from ...values.null import NullValue
from ...values.list import ListValue
from ...values.number import NumberValue
from ...values.base import RuntimeValue

def list_append(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_append requires a list and a value")
    lst = args[0]
    val = args[1]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.append(val)
    return NullValue()

def list_length(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_length requires a list")
    lst = args[0]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.length()

def list_get(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_get requires a list and an index")
    lst = args[0]
    idx = args[1]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.get(idx)

def list_set(args: list, vm) -> RuntimeValue:
    if len(args) < 3:
        raise Exception("list_set requires a list, an index, and a value")
    lst = args[0]
    idx = args[1]
    val = args[2]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.set(idx, val)
    return NullValue()

def list_remove(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_remove requires a list and an index")
    lst = args[0]
    idx = args[1]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.remove(idx)
    return NullValue()

def list_contains(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_contains requires a list and a value")
    lst = args[0]
    val = args[1]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.contains(val)

def register_list_stdlib(registry):
    registry.register("list_append", list_append)
    registry.register("list_length", list_length)
    registry.register("list_get", list_get)
    registry.register("list_set", list_set)
    registry.register("list_remove", list_remove)
    registry.register("list_contains", list_contains)
