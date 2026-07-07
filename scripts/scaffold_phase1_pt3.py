import os

runtime_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules"

def write_file(path, content):
    with open(os.path.join(runtime_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

write_file("logging_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue

def register_logging_lib(registry: StdLibRegistry):
    def fn_info(args, vm):
        if args: print(f"[INFO] {args[0].stringify()}")
        return NullValue()
    registry.register("logging::info", fn_info)
    
    def fn_warn(args, vm):
        if args: print(f"[WARN] {args[0].stringify()}")
        return NullValue()
    registry.register("logging::warn", fn_warn)

    def fn_error(args, vm):
        if args: print(f"[ERROR] {args[0].stringify()}")
        return NullValue()
    registry.register("logging::error", fn_error)
""")

write_file("testing_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.boolean import BooleanValue
from ...values.exception import AssertionException

def register_testing_lib(registry: StdLibRegistry):
    def fn_assert(args, vm):
        if not args: return BooleanValue(False)
        if not args[0].truthy():
            msg = args[1].to_python() if len(args) > 1 else "Assertion failed"
            raise Exception(f"AssertionException: {msg}") # In real VM, throw AAYU exception
        return BooleanValue(True)
    registry.register("testing::assert", fn_assert)
""")

write_file("compression_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
import gzip
import base64

def register_compression_lib(registry: StdLibRegistry):
    def fn_gzip_compress(args, vm):
        if not args: return NullValue()
        data = args[0].to_python().encode('utf-8')
        compressed = gzip.compress(data)
        return make_string(vm, base64.b64encode(compressed).decode('utf-8'))
    registry.register("compression::gzip", fn_gzip_compress)
""")

write_file("concurrency_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
import threading

def register_concurrency_lib(registry: StdLibRegistry):
    def fn_spawn(args, vm):
        if not args: return NullValue()
        # args[0] should be a function
        func = args[0]
        def run_thread():
            # In a real VM, we need a thread-safe context
            pass 
        t = threading.Thread(target=run_thread)
        t.start()
        return NullValue()
    registry.register("concurrency::spawn", fn_spawn)
""")

print("Created remaining libs")
