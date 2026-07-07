import os
import shutil
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.boolean import BooleanValue

def create_string(vm, text):
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def register_file_lib(registry: StdLibRegistry):
    def fn_read(args, vm):
        try:
            path = args[0].to_python()
            # Handle binary vs utf-8 based on optional second arg
            mode = 'r'
            encoding = 'utf-8'
            if len(args) > 1 and args[1].to_python() == "binary":
                mode = 'rb'
                encoding = None
            
            if mode == 'rb':
                with open(path, mode) as f:
                    return create_string(vm, f.read().decode('latin-1')) # fallback for binary string storage
            else:
                with open(path, mode, encoding=encoding) as f:
                    return create_string(vm, f.read())
        except FileNotFoundError:
            return create_string(vm, "error: file not found")
        except PermissionError:
            return create_string(vm, "error: permission denied")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")
            
    def fn_write(args, vm):
        try:
            path = args[0].to_python()
            content = args[1].to_python()
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return BooleanValue(True)
        except PermissionError:
            return create_string(vm, "error: permission denied")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")
            
    def fn_append(args, vm):
        try:
            path = args[0].to_python()
            content = args[1].to_python()
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content)
            return BooleanValue(True)
        except PermissionError:
            return create_string(vm, "error: permission denied")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")
            
    def fn_delete(args, vm):
        try:
            path = args[0].to_python()
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return BooleanValue(True)
        except FileNotFoundError:
            return create_string(vm, "error: file not found")
        except PermissionError:
            return create_string(vm, "error: permission denied")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")

    def fn_mkdir(args, vm):
        try:
            path = args[0].to_python()
            os.makedirs(path, exist_ok=True)
            return BooleanValue(True)
        except PermissionError:
            return create_string(vm, "error: permission denied")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")

    def fn_exists(args, vm):
        return BooleanValue(os.path.exists(args[0].to_python()))
        
    registry.register("fs::read", fn_read)
    registry.register("fs::write", fn_write)
    registry.register("fs::append", fn_append)
    registry.register("fs::delete", fn_delete)
    registry.register("fs::mkdir", fn_mkdir)
    registry.register("fs::exists", fn_exists)
