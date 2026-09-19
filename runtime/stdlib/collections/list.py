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

def list_append(args: list, vm):
    if len(args) < 2:
        raise Exception("list_append requires a list and a value")
    lst = args[0]
    val = args[1]
    if isinstance(lst, list):
        lst.append(val)
        return None
    lst.append(val)
    return None

def list_length(args: list, vm):
    if len(args) < 1:
        raise Exception("list_length requires a list")
    lst = args[0]
    if isinstance(lst, list):
        return len(lst)
    return len(lst.to_python()) if hasattr(lst, 'to_python') else 0

def list_get(args: list, vm):
    if len(args) < 2:
        raise Exception("list_get requires a list and an index")
    lst = args[0]
    idx = args[1]
    idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
    if isinstance(lst, list):
        return lst[idx_val]
    return lst.get(idx_val)

def list_set(args: list, vm):
    if len(args) < 3:
        raise Exception("list_set requires a list, an index, and a value")
    lst = args[0]
    idx = args[1]
    val = args[2]
    idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
    if isinstance(lst, list):
        lst[idx_val] = val
        return None
    lst.set(idx_val, val)
    return None

def list_remove(args: list, vm):
    if len(args) < 2:
        raise Exception("list_remove requires a list and an index")
    lst = args[0]
    idx = args[1]
    idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
    if isinstance(lst, list):
        lst.pop(idx_val)
        return None
    lst.remove(idx_val)
    return None

def list_contains(args: list, vm):
    if len(args) < 2:
        raise Exception("list_contains requires a list and a value")
    lst = args[0]
    val = args[1]
    val_py = val.to_python() if hasattr(val, 'to_python') else val
    if isinstance(lst, list):
        return val_py in lst
    lst_py = lst.to_python() if hasattr(lst, 'to_python') else []
    return val_py in lst_py

def list_pop(args: list, vm):
    if len(args) < 1:
        raise Exception("list_pop requires a list")
    lst = args[0]
    if isinstance(lst, list):
        return lst.pop()
    val = lst._get_payload().pop()
    return val

def list_insert(args: list, vm):
    if len(args) < 3:
        raise Exception("list_insert requires a list, an index, and a value")
    lst = args[0]
    idx = args[1]
    val = args[2]
    idx_val = int(idx.to_python() if hasattr(idx, 'to_python') else idx)
    if isinstance(lst, list):
        lst.insert(idx_val, val)
        return None
    lst._get_payload().insert(idx_val, val)
    return None

def list_reverse(args: list, vm):
    if len(args) < 1:
        raise Exception("list_reverse requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.reverse()
        return None
    lst._get_payload().reverse()
    return None

def list_sort(args: list, vm):
    if len(args) < 1:
        raise Exception("list_sort requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.sort(key=lambda x: x.to_python() if hasattr(x, 'to_python') else x)
        return None
    lst._get_payload().sort(key=lambda x: x.to_python() if hasattr(x, 'to_python') else x)
    return None

def list_clear(args: list, vm):
    if len(args) < 1:
        raise Exception("list_clear requires a list")
    lst = args[0]
    if isinstance(lst, list):
        lst.clear()
        return None
    lst._get_payload().clear()
    return None

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
