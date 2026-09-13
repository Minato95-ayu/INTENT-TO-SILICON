
import ctypes
import os

def py_call(module_name, func_name, *args):
    """AAYU VM FFI Native Call Handler"""
    import importlib
    mod = importlib.import_module(module_name)
    func = getattr(mod, func_name)
    return func(*args)

# Simulating an AAYU VM Call
print("[AAYU FFI] Calling Python math.sqrt(144) natively...")
result = py_call("math", "sqrt", 144)
print(f"[AAYU FFI] Result: {result}")

