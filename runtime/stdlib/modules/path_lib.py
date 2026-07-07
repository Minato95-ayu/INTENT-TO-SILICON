"""
=============================================================================
FILE: path_lib.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ..helpers import make_string, make_list, make_map
from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
import os

def register_path_lib(registry: StdLibRegistry):
    def fn_join(args, vm):
        if not args: return NullValue()
        paths = [a.to_python() for a in args]
        return make_string(vm, os.path.join(*paths))
    registry.register("path::join", fn_join)
    
    def fn_dirname(args, vm):
        if not args: return NullValue()
        return make_string(vm, os.path.dirname(args[0].to_python()))
    registry.register("path::dirname", fn_dirname)
    
    def fn_basename(args, vm):
        if not args: return NullValue()
        return make_string(vm, os.path.basename(args[0].to_python()))
    registry.register("path::basename", fn_basename)
    
    def fn_extension(args, vm):
        if not args: return NullValue()
        _, ext = os.path.splitext(args[0].to_python())
        return make_string(vm, ext)
    registry.register("path::extension", fn_extension)
