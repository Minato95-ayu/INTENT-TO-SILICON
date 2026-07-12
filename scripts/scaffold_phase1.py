import os

runtime_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime"

def write_file(path, content):
    full_path = os.path.join(runtime_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Scaffolding Phase 1 Standard Library...")

write_file("values/queue_val.py", """\
from .base import RuntimeValue
from collections import deque

class QueueValue(RuntimeValue):
    def __init__(self, elements=None):
        self.elements = deque(elements) if elements else deque()
        
    def type_name(self) -> str:
        return "Queue"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, QueueValue): return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return QueueValue(list(self.elements))
        
    def stringify(self) -> str:
        return f"Queue({list(self.elements)})"
        
    def to_python(self):
        return list(self.elements)
""")

write_file("values/stack_val.py", """\
from .base import RuntimeValue

class StackValue(RuntimeValue):
    def __init__(self, elements=None):
        self.elements = elements if elements else []
        
    def type_name(self) -> str:
        return "Stack"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, StackValue): return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return StackValue(list(self.elements))
        
    def stringify(self) -> str:
        return f"Stack({self.elements})"
        
    def to_python(self):
        return self.elements
""")

write_file("values/heap_val.py", """\
from .base import RuntimeValue
import heapq

class HeapValue(RuntimeValue):
    def __init__(self, elements=None):
        self.elements = elements if elements else []
        heapq.heapify(self.elements)
        
    def type_name(self) -> str:
        return "Heap"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, HeapValue): return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return HeapValue(list(self.elements))
        
    def stringify(self) -> str:
        return f"Heap({self.elements})"
        
    def to_python(self):
        return self.elements
""")

write_file("stdlib/modules/database_lib.py", """\
from ..helpers import make_string, make_list, make_map
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.boolean import BooleanValue
from ...values.string import StringValue
from ...values.number import NumberValue
import sqlite3
import json

def register_database_lib(registry: StdLibRegistry):
    def fn_sqlite_query(args, vm):
        if len(args) < 2: return NullValue()
        db_path = args[0].to_python()
        query = args[1].to_python()
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description] if cur.description else []
        conn.commit()
        conn.close()
        
        result = []
        for row in rows:
            obj = {}
            for i, val in enumerate(row):
                obj[cols[i]] = val
            result.append(obj)
            
        return make_list(vm, [make_map(vm, {make_string(vm, k): make_string(vm, str(v)) for k, v in r.items()}) for r in result])
        
    registry.register("sqlite::query", fn_sqlite_query)
""")

write_file("stdlib/modules/regex_lib.py", """\
from ..helpers import make_string, make_list
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.boolean import BooleanValue
import re

def register_regex_lib(registry: StdLibRegistry):
    def fn_match(args, vm):
        if len(args) < 2: return BooleanValue(False)
        pattern = args[0].to_python()
        text = args[1].to_python()
        return BooleanValue(bool(re.match(pattern, text)))
    registry.register("regex::match", fn_match)
""")

write_file("stdlib/modules/env_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
import os

def register_env_lib(registry: StdLibRegistry):
    def fn_get(args, vm):
        if not args: return NullValue()
        val = os.getenv(args[0].to_python())
        if val is None: return NullValue()
        return make_string(vm, val)
    registry.register("env::get", fn_get)
""")

write_file("stdlib/modules/process_lib.py", """\
from ..helpers import make_string, make_map
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.number import NumberValue
import subprocess

def register_process_lib(registry: StdLibRegistry):
    def fn_exec(args, vm):
        if not args: return NullValue()
        cmd = args[0].to_python()
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return make_map(vm, {
                make_string(vm, "stdout"): make_string(vm, res.stdout),
                make_string(vm, "stderr"): make_string(vm, res.stderr),
                make_string(vm, "code"): NumberValue(res.returncode)
            })
        except Exception as e:
            return make_map(vm, {
                make_string(vm, "stdout"): make_string(vm, ""),
                make_string(vm, "stderr"): make_string(vm, str(e)),
                make_string(vm, "code"): NumberValue(-1)
            })
    registry.register("process::exec", fn_exec)
""")

print("Finished scaffolding Phase 1 Standard Library.")
