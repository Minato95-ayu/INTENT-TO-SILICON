"""
=============================================================================
FILE: scaffold2.py
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

math_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.boolean import BooleanValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.exception import RuntimeException
import math
import random

def register_math_lib(registry: StdLibRegistry):
    def fn_sqrt(args, vm):
        if not args: return NullValue()
        return NumberValue(math.sqrt(args[0].to_python()))
    registry.register("math::sqrt", fn_sqrt)
    
    def fn_pow(args, vm):
        if len(args) < 2: return NullValue()
        return NumberValue(math.pow(args[0].to_python(), args[1].to_python()))
    registry.register("math::pow", fn_pow)
    
    def fn_abs(args, vm):
        if not args: return NullValue()
        return NumberValue(abs(args[0].to_python()))
    registry.register("math::abs", fn_abs)

    def fn_min(args, vm):
        if len(args) < 2: return NullValue()
        return NumberValue(min(args[0].to_python(), args[1].to_python()))
    registry.register("math::min", fn_min)

    def fn_max(args, vm):
        if len(args) < 2: return NullValue()
        return NumberValue(max(args[0].to_python(), args[1].to_python()))
    registry.register("math::max", fn_max)

    def fn_round(args, vm):
        if not args: return NullValue()
        return NumberValue(round(args[0].to_python()))
    registry.register("math::round", fn_round)

    def fn_floor(args, vm):
        if not args: return NullValue()
        return NumberValue(math.floor(args[0].to_python()))
    registry.register("math::floor", fn_floor)

    def fn_ceil(args, vm):
        if not args: return NullValue()
        return NumberValue(math.ceil(args[0].to_python()))
    registry.register("math::ceil", fn_ceil)
"""

string_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.boolean import BooleanValue
from ...values.null import NullValue
from ...values.list import ListValue

def register_string_lib(registry: StdLibRegistry):
    def fn_split(args, vm):
        if len(args) < 2: return NullValue()
        parts = args[0].to_python().split(args[1].to_python())
        return ListValue([StringValue(p) for p in parts])
    registry.register("string::split", fn_split)
    
    def fn_trim(args, vm):
        if not args: return NullValue()
        return StringValue(args[0].to_python().strip())
    registry.register("string::trim", fn_trim)
    
    def fn_replace(args, vm):
        if len(args) < 3: return NullValue()
        return StringValue(args[0].to_python().replace(args[1].to_python(), args[2].to_python()))
    registry.register("string::replace", fn_replace)
    
    def fn_upper(args, vm):
        if not args: return NullValue()
        return StringValue(args[0].to_python().upper())
    registry.register("string::upper", fn_upper)
    
    def fn_lower(args, vm):
        if not args: return NullValue()
        return StringValue(args[0].to_python().lower())
    registry.register("string::lower", fn_lower)
    
    def fn_contains(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[1].to_python() in args[0].to_python())
    registry.register("string::contains", fn_contains)
    
    def fn_starts_with(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[0].to_python().startswith(args[1].to_python()))
    registry.register("string::starts_with", fn_starts_with)
    
    def fn_ends_with(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[0].to_python().endswith(args[1].to_python()))
    registry.register("string::ends_with", fn_ends_with)
"""

list_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.null import NullValue
from ...values.list import ListValue

def register_list_lib(registry: StdLibRegistry):
    def fn_push(args, vm):
        if len(args) < 2: return NullValue()
        args[0].elements.append(args[1])
        return args[0]
    registry.register("list::push", fn_push)
    
    def fn_pop(args, vm):
        if not args: return NullValue()
        if not args[0].elements: return NullValue()
        return args[0].elements.pop()
    registry.register("list::pop", fn_pop)
    
    def fn_insert(args, vm):
        if len(args) < 3: return NullValue()
        args[0].elements.insert(int(args[1].to_python()), args[2])
        return args[0]
    registry.register("list::insert", fn_insert)
    
    def fn_remove(args, vm):
        if len(args) < 2: return NullValue()
        idx = int(args[1].to_python())
        if 0 <= idx < len(args[0].elements):
            return args[0].elements.pop(idx)
        return NullValue()
    registry.register("list::remove", fn_remove)
    
    def fn_sort(args, vm):
        if not args: return NullValue()
        # Simplistic sort based on native python comparison
        try:
            args[0].elements.sort(key=lambda x: x.to_python())
        except Exception:
            pass
        return args[0]
    registry.register("list::sort", fn_sort)
    
    def fn_reverse(args, vm):
        if not args: return NullValue()
        args[0].elements.reverse()
        return args[0]
    registry.register("list::reverse", fn_reverse)
    
    def fn_length(args, vm):
        if not args: return NullValue()
        return NumberValue(len(args[0].elements))
    registry.register("list::length", fn_length)
"""

map_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.boolean import BooleanValue
from ...values.null import NullValue

def register_map_lib(registry: StdLibRegistry):
    def fn_put(args, vm):
        if len(args) < 3: return NullValue()
        args[0].elements[args[1].to_python()] = args[2]
        return args[0]
    registry.register("map::put", fn_put)
    
    def fn_get(args, vm):
        if len(args) < 2: return NullValue()
        return args[0].elements.get(args[1].to_python(), NullValue())
    registry.register("map::get", fn_get)
    
    def fn_remove(args, vm):
        if len(args) < 2: return NullValue()
        key = args[1].to_python()
        if key in args[0].elements:
            return args[0].elements.pop(key)
        return NullValue()
    registry.register("map::remove", fn_remove)
    
    def fn_contains(args, vm):
        if len(args) < 2: return NullValue()
        return BooleanValue(args[1].to_python() in args[0].elements)
    registry.register("map::contains", fn_contains)
"""

file_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.boolean import BooleanValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.exception import RuntimeException
import os

def register_file_lib(registry: StdLibRegistry):
    def fn_read(args, vm):
        if not args: return NullValue()
        path = args[0].to_python()
        if not os.path.exists(path):
            return NullValue()
        with open(path, 'r', encoding='utf-8') as f:
            return StringValue(f.read())
    registry.register("file::read", fn_read)
    
    def fn_write(args, vm):
        if len(args) < 2: return NullValue()
        with open(args[0].to_python(), 'w', encoding='utf-8') as f:
            f.write(args[1].to_python())
        return NullValue()
    registry.register("file::write", fn_write)
    
    def fn_append(args, vm):
        if len(args) < 2: return NullValue()
        with open(args[0].to_python(), 'a', encoding='utf-8') as f:
            f.write(args[1].to_python())
        return NullValue()
    registry.register("file::append", fn_append)
    
    def fn_exists(args, vm):
        if not args: return NullValue()
        return BooleanValue(os.path.exists(args[0].to_python()))
    registry.register("file::exists", fn_exists)
    
    def fn_delete(args, vm):
        if not args: return NullValue()
        path = args[0].to_python()
        if os.path.exists(path):
            os.remove(path)
            return BooleanValue(True)
        return BooleanValue(False)
    registry.register("file::delete", fn_delete)
    
    def fn_mkdir(args, vm):
        if not args: return NullValue()
        os.makedirs(args[0].to_python(), exist_ok=True)
        return NullValue()
    registry.register("file::mkdir", fn_mkdir)
"""

path_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
import os

def register_path_lib(registry: StdLibRegistry):
    def fn_join(args, vm):
        if not args: return NullValue()
        paths = [a.to_python() for a in args]
        return StringValue(os.path.join(*paths))
    registry.register("path::join", fn_join)
    
    def fn_dirname(args, vm):
        if not args: return NullValue()
        return StringValue(os.path.dirname(args[0].to_python()))
    registry.register("path::dirname", fn_dirname)
    
    def fn_basename(args, vm):
        if not args: return NullValue()
        return StringValue(os.path.basename(args[0].to_python()))
    registry.register("path::basename", fn_basename)
    
    def fn_extension(args, vm):
        if not args: return NullValue()
        _, ext = os.path.splitext(args[0].to_python())
        return StringValue(ext)
    registry.register("path::extension", fn_extension)
"""

json_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.number import NumberValue
from ...values.boolean import BooleanValue
import json

def py_to_aayu(val):
    if isinstance(val, dict):
        return MapValue({k: py_to_aayu(v) for k, v in val.items()})
    elif isinstance(val, list):
        return ListValue([py_to_aayu(v) for v in val])
    elif isinstance(val, (int, float)):
        return NumberValue(float(val))
    elif isinstance(val, bool):
        return BooleanValue(val)
    elif isinstance(val, str):
        return StringValue(val)
    return NullValue()

def register_json_lib(registry: StdLibRegistry):
    def fn_encode(args, vm):
        if not args: return NullValue()
        return StringValue(json.dumps(args[0].to_python()))
    registry.register("json::encode", fn_encode)
    
    def fn_decode(args, vm):
        if not args: return NullValue()
        try:
            parsed = json.loads(args[0].to_python())
            return py_to_aayu(parsed)
        except:
            return NullValue()
    registry.register("json::decode", fn_decode)
"""

time_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.null import NullValue
import time
import datetime

def register_time_lib(registry: StdLibRegistry):
    def fn_now(args, vm):
        return StringValue(datetime.datetime.now().isoformat())
    registry.register("time::now", fn_now)
    
    def fn_sleep(args, vm):
        if not args: return NullValue()
        time.sleep(args[0].to_python())
        return NullValue()
    registry.register("time::sleep", fn_sleep)
    
    def fn_timestamp(args, vm):
        return NumberValue(time.time())
    registry.register("time::timestamp", fn_timestamp)
"""

random_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.null import NullValue
import random

def register_random_lib(registry: StdLibRegistry):
    def fn_int(args, vm):
        if len(args) < 2: return NullValue()
        return NumberValue(random.randint(int(args[0].to_python()), int(args[1].to_python())))
    registry.register("random::int", fn_int)
    
    def fn_float(args, vm):
        return NumberValue(random.random())
    registry.register("random::float", fn_float)
    
    def fn_choice(args, vm):
        if not args: return NullValue()
        elements = args[0].elements
        if not elements: return NullValue()
        return random.choice(elements)
    registry.register("random::choice", fn_choice)
"""

http_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.map import MapValue
from ...values.number import NumberValue
from ...values.string import StringValue
from ...values.null import NullValue
import urllib.request
import urllib.error
import json

def _make_request(method, url, data=None, headers=None):
    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    if data:
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
            req.add_header('Content-Type', 'application/json')
            
    try:
        with urllib.request.urlopen(req, data=data) as response:
            body = response.read().decode('utf-8')
            return MapValue({
                "status": NumberValue(response.status),
                "body": StringValue(body)
            })
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return MapValue({
            "status": NumberValue(e.code),
            "body": StringValue(body)
        })
    except Exception as e:
        return MapValue({
            "status": NumberValue(500),
            "body": StringValue(str(e))
        })

def register_http_lib(registry: StdLibRegistry):
    def fn_get(args, vm):
        if not args: return NullValue()
        url = args[0].to_python()
        return _make_request('GET', url)
    registry.register("http::get", fn_get)
    
    def fn_post(args, vm):
        if len(args) < 2: return NullValue()
        url = args[0].to_python()
        data = args[1].to_python()
        return _make_request('POST', url, data=data)
    registry.register("http::post", fn_post)
    
    def fn_put(args, vm):
        if len(args) < 2: return NullValue()
        url = args[0].to_python()
        data = args[1].to_python()
        return _make_request('PUT', url, data=data)
    registry.register("http::put", fn_put)
    
    def fn_delete(args, vm):
        if not args: return NullValue()
        url = args[0].to_python()
        return _make_request('DELETE', url)
    registry.register("http::delete", fn_delete)
"""

crypto_impl = """from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
import hashlib
import uuid

def register_crypto_lib(registry: StdLibRegistry):
    def fn_sha256(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return StringValue(hashlib.sha256(s.encode('utf-8')).hexdigest())
    registry.register("crypto::sha256", fn_sha256)
    
    def fn_md5(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return StringValue(hashlib.md5(s.encode('utf-8')).hexdigest())
    registry.register("crypto::md5", fn_md5)
    
    def fn_uuid(args, vm):
        return StringValue(str(uuid.uuid4()))
    registry.register("crypto::uuid", fn_uuid)
"""

with open(os.path.join(MODULES_DIR, "math_lib.py"), "w", encoding="utf-8") as f: f.write(math_impl)
with open(os.path.join(MODULES_DIR, "string_lib.py"), "w", encoding="utf-8") as f: f.write(string_impl)
with open(os.path.join(MODULES_DIR, "list_lib.py"), "w", encoding="utf-8") as f: f.write(list_impl)
with open(os.path.join(MODULES_DIR, "map_lib.py"), "w", encoding="utf-8") as f: f.write(map_impl)
with open(os.path.join(MODULES_DIR, "file_lib.py"), "w", encoding="utf-8") as f: f.write(file_impl)
with open(os.path.join(MODULES_DIR, "path_lib.py"), "w", encoding="utf-8") as f: f.write(path_impl)
with open(os.path.join(MODULES_DIR, "json_lib.py"), "w", encoding="utf-8") as f: f.write(json_impl)
with open(os.path.join(MODULES_DIR, "time_lib.py"), "w", encoding="utf-8") as f: f.write(time_impl)
with open(os.path.join(MODULES_DIR, "random_lib.py"), "w", encoding="utf-8") as f: f.write(random_impl)
with open(os.path.join(MODULES_DIR, "http_lib.py"), "w", encoding="utf-8") as f: f.write(http_impl)
with open(os.path.join(MODULES_DIR, "crypto_lib.py"), "w", encoding="utf-8") as f: f.write(crypto_impl)

print("Generated full implementations")
