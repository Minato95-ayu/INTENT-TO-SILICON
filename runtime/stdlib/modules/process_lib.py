import subprocess
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj.id, vm.heap)

def register_process_lib(registry: StdLibRegistry):
    def fn_exec(args, vm):
        try:
            cmd = args[0].to_python()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return create_string(vm, result.stdout)
        except Exception:
            return NullValue()
            
    registry.register("process::exec", fn_exec)
