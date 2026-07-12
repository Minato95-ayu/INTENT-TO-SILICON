"""
=============================================================================
FILE: scaffold.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os

MODULES_DIR = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules"

modules = {
    "math_lib": [
        "sqrt", "pow", "abs", "min", "max", "round", "floor", "ceil"
    ],
    "string_lib": [
        "split", "trim", "replace", "upper", "lower", "contains", "starts_with", "ends_with"
    ],
    "list_lib": [
        "push", "pop", "insert", "remove", "sort", "reverse", "length"
    ],
    "map_lib": [
        "put", "get", "remove", "contains"
    ],
    "file_lib": [
        "read", "write", "append", "exists", "delete", "mkdir"
    ],
    "path_lib": [
        "join", "dirname", "basename", "extension"
    ],
    "json_lib": [
        "encode", "decode"
    ],
    "time_lib": [
        "now", "sleep", "timestamp"
    ],
    "random_lib": [
        "int", "float", "choice"
    ],
    "http_lib": [
        "get", "post", "put", "delete"
    ],
    "crypto_lib": [
        "sha256", "md5", "uuid"
    ]
}

template = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.boolean import BooleanValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.exception import RuntimeException

def register_{mod_name}(registry: StdLibRegistry):
{functions}
"""

func_template = """
    def fn_{func_name}(args, vm):
        # TODO: Implement {ns}::{func_name}
        return NullValue()
        
    registry.register("{ns}::{func_name}", fn_{func_name})
"""

for mod_name, funcs in modules.items():
    ns = mod_name.replace("_lib", "")
    funcs_code = ""
    for func in funcs:
        funcs_code += func_template.format(func_name=func, ns=ns)
    
    file_content = template.format(mod_name=mod_name, functions=funcs_code)
    with open(os.path.join(MODULES_DIR, f"{mod_name}.py"), "w", encoding="utf-8") as f:
        f.write(file_content)

# Also create __init__.py
with open(os.path.join(MODULES_DIR, "__init__.py"), "w", encoding="utf-8") as f:
    for mod_name in modules.keys():
        f.write(f"from .{mod_name} import register_{mod_name}\n")

print("Generated modules")
