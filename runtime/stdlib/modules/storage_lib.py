"""
Storage Module for AAYU Standard Library
Provides storage.get() and storage.set() for local storage abstraction.
"""
import os
import json

_STORAGE_FILE = ".aayu/storage.json"

def _ensure_storage():
    os.makedirs(os.path.dirname(os.path.abspath(_STORAGE_FILE)), exist_ok=True)
    if not os.path.exists(_STORAGE_FILE):
        with open(_STORAGE_FILE, "w") as f:
            json.dump({}, f)

def _read_storage():
    _ensure_storage()
    try:
        with open(_STORAGE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_storage(data):
    _ensure_storage()
    with open(_STORAGE_FILE, "w") as f:
        json.dump(data, f)

def storage_get(args, vm):
    if not args: return None
    key = args[0]
    data = _read_storage()
    return data.get(key, None)

def storage_set(args, vm):
    if len(args) < 2: return False
    key, value = args[0], args[1]
    data = _read_storage()
    data[key] = value
    _write_storage(data)
    return True
    
def storage_remove(args, vm):
    if not args: return False
    key = args[0]
    data = _read_storage()
    if key in data:
        del data[key]
        _write_storage(data)
        return True
    return False

def register_storage_lib(registry):
    registry.register("storage.get", storage_get)
    registry.register("storage.set", storage_set)
    registry.register("storage.remove", storage_remove)
