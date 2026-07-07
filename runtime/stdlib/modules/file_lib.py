import os
import shutil
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.boolean import BooleanValue

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj.id, vm.heap)

def register_file_lib(registry: StdLibRegistry):
    def fn_read(args, vm):
        try:
            with open(args[0].to_python(), 'r') as f:
                return create_string(vm, f.read())
        except Exception:
            return NullValue()
            
    def fn_write(args, vm):
        try:
            with open(args[0].to_python(), 'w') as f:
                f.write(args[1].to_python())
            return BooleanValue(True)
        except Exception:
            return BooleanValue(False)
            
    def fn_exists(args, vm):
        return BooleanValue(os.path.exists(args[0].to_python()))
        
    registry.register("fs::read", fn_read)
    registry.register("fs::write", fn_write)
    registry.register("fs::exists", fn_exists)
