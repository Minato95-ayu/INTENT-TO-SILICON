import os
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj.id, vm.heap)

def register_env_lib(registry: StdLibRegistry):
    def fn_get(args, vm):
        try:
            val = os.environ.get(args[0].to_python())
            if val is None:
                return NullValue()
            return create_string(vm, val)
        except Exception:
            return NullValue()
            
    registry.register("env::get", fn_get)
