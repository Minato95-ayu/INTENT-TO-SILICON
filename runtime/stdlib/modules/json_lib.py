import json
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.number import NumberValue
from ...values.boolean import BooleanValue

def create_string(vm, text):
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def py_to_aayu(py_val, vm):
    if isinstance(py_val, dict):
        d = {k: py_to_aayu(v, vm) for k, v in py_val.items()}
        obj = vm.memory.heap.allocate("map", d)
        return MapValue(obj.id, vm.memory.heap)
    elif isinstance(py_val, list):
        l = [py_to_aayu(x, vm) for x in py_val]
        obj = vm.memory.heap.allocate("list", l)
        return ListValue(obj.id, vm.memory.heap)
    elif isinstance(py_val, str):
        return create_string(vm, py_val)
    elif isinstance(py_val, (int, float)):
        return NumberValue(float(py_val))
    elif isinstance(py_val, bool):
        return BooleanValue(py_val)
    return NullValue()

def aayu_to_py(aayu_val):
    if hasattr(aayu_val, 'to_python'):
        return aayu_val.to_python()
    return None

def register_json_lib(registry: StdLibRegistry):
    def fn_parse(args, vm):
        try:
            py_val = json.loads(args[0].to_python())
            return py_to_aayu(py_val, vm)
        except Exception:
            return NullValue()
            
    def fn_stringify(args, vm):
        try:
            py_val = aayu_to_py(args[0])
            return create_string(vm, json.dumps(py_val))
        except Exception:
            return NullValue()
            
    registry.register("json::parse", fn_parse)
    registry.register("json::stringify", fn_stringify)
