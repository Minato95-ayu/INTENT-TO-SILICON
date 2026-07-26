"""
=============================================================================
FILE: list.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ...values.null import NullValue
from ...values.list import ListValue
from ...values.number import NumberValue
from ...values.base import RuntimeValue

def list_append(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_append requires a list and a value")
    lst = args[0]
    val = args[1]
    if isinstance(lst, list):
        lst.append(val)
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.append(val)
    return NullValue()

def list_length(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_length requires a list")
    lst = args[0]
    if isinstance(lst, list):
        return NumberValue(len(lst))
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.length()

def list_get(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_get requires a list and an index")
    lst = args[0]
    idx = args[1]
    if isinstance(lst, list):
        idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
        return lst[idx_val]
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.get(idx)

def list_set(args: list, vm) -> RuntimeValue:
    if len(args) < 3:
        raise Exception("list_set requires a list, an index, and a value")
    lst = args[0]
    idx = args[1]
    val = args[2]
    if isinstance(lst, list):
        idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
        lst[idx_val] = val
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.set(idx, val)
    return NullValue()

def list_remove(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_remove requires a list and an index")
    lst = args[0]
    idx = args[1]
    if isinstance(lst, list):
        idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
        lst.pop(idx_val)
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst.remove(idx)
    return NullValue()

def list_contains(args: list, vm) -> RuntimeValue:
    if len(args) < 2:
        raise Exception("list_contains requires a list and a value")
    lst = args[0]
    val = args[1]
    if isinstance(lst, list):
        return val in lst
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    return lst.contains(val)

def list_pop(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_pop requires a list")
    lst = args[0]
    if isinstance(lst, list):
        return lst.pop()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    val = lst._get_payload().pop()
    return val

def list_insert(args: list, vm) -> RuntimeValue:
    if len(args) < 3:
        raise Exception("list_insert requires a list, an index, and a value")
    lst = args[0]
    idx = args[1]
    val = args[2]
    if isinstance(lst, list):
        idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
        lst.insert(idx_val, val)
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    if not isinstance(idx, NumberValue):
        raise Exception(f"Expected index to be a number")
    lst._get_payload().insert(int(idx.to_python()), val)
    return NullValue()

def list_reverse(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_reverse requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.reverse()
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst._get_payload().reverse()
    return NullValue()

def list_sort(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_sort requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.sort(key=lambda x: x.to_python() if hasattr(x, 'to_python') else x)
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    
    # Simple sort based on underlying python values
    lst._get_payload().sort(key=lambda x: x.to_python())
    return NullValue()

def list_clear(args: list, vm) -> RuntimeValue:
    if len(args) < 1:
        raise Exception("list_clear requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.clear()
        return NullValue()
    if not isinstance(lst, ListValue):
        raise Exception(f"Expected a list, got {lst.type_name()}")
    lst._get_payload().clear()
    return NullValue()

def register_list_stdlib(registry):
    registry.register("list_append", list_append)
    registry.register("list_length", list_length)
    registry.register("list_get", list_get)
    registry.register("list_set", list_set)
    registry.register("list_remove", list_remove)
    registry.register("list_contains", list_contains)
    registry.register("list_pop", list_pop)
    registry.register("list_insert", list_insert)
    registry.register("list_reverse", list_reverse)
    registry.register("list_sort", list_sort)
    registry.register("list_clear", list_clear)
