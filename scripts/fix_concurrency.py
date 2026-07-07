import os

concurrency_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\concurrency_lib.py'
with open(concurrency_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.function import FunctionValue
import threading

def register_concurrency_lib(registry: StdLibRegistry):
    def fn_spawn(args, vm):
        if not args: return NullValue()
        func = args[0]
        if not isinstance(func, FunctionValue):
            return NullValue()
        
        def run_thread():
            # Minimal thread safe execution for the VM
            try:
                # Assuming simple functions for now
                if hasattr(func, 'call'):
                    func.call([], vm)
            except Exception as e:
                print(f"[Concurrency Error] {e}")

        t = threading.Thread(target=run_thread)
        t.start()
        return NullValue()
    registry.register("concurrency::spawn", fn_spawn)
"""

with open(concurrency_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed concurrency_lib.py")
