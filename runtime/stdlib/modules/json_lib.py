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

def py_to_aayu(py_val, vm, depth=0):
    if depth > 200:
        return create_string(vm, "error: json too deep")
        
    if isinstance(py_val, dict):
        d = {k: py_to_aayu(v, vm, depth+1) for k, v in py_val.items()}
        obj = vm.memory.heap.allocate("map", d)
        return MapValue(obj.id, vm.memory.heap)
    elif isinstance(py_val, list):
        l = [py_to_aayu(x, vm, depth+1) for x in py_val]
        obj = vm.memory.heap.allocate("list", l)
        return ListValue(obj.id, vm.memory.heap)
    elif isinstance(py_val, str):
        return create_string(vm, py_val)
    elif isinstance(py_val, (int, float)):
        return NumberValue(float(py_val))
    elif isinstance(py_val, bool):
        return BooleanValue(py_val)
    return NullValue()

def aayu_to_py(aayu_val, seen=None):
    if seen is None:
        seen = set()
        
    # Protection against circular references during stringify
    if id(aayu_val) in seen:
        return "<circular>"
    seen.add(id(aayu_val))
    
    if isinstance(aayu_val, MapValue):
        # We need a proper map items fetcher, assuming it acts like dictionary payload
        payload = aayu_val._get_payload()
        return {k: aayu_to_py(v, seen) for k, v in payload.items()}
    elif isinstance(aayu_val, ListValue):
        payload = aayu_val._get_payload()
        return [aayu_to_py(x, seen) for x in payload]
    elif hasattr(aayu_val, 'to_python'):
        return aayu_val.to_python()
    return None

def register_json_lib(registry: StdLibRegistry):
    def fn_parse(args, vm):
        try:
            # Need to decode from AAYU string if possible, or just to_python
            py_str = args[0].to_python()
            py_val = json.loads(py_str)
            return py_to_aayu(py_val, vm)
        except json.JSONDecodeError as e:
            return create_string(vm, f"error: invalid json: {e}")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")
            
    def fn_stringify(args, vm):
        try:
            py_val = aayu_to_py(args[0])
            # Handle unicode correctly, ensuring ASCII is bypassed
            return create_string(vm, json.dumps(py_val, ensure_ascii=False))
        except Exception as e:
            print("Stringify Error:", str(e))
            return create_string(vm, f"error: stringify failed: {str(e)}")
            
    registry.register("json::parse", fn_parse)
    registry.register("json::stringify", fn_stringify)
