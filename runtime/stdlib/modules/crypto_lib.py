import hashlib
import secrets
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj.id, vm.heap)

def register_crypto_lib(registry: StdLibRegistry):
    def fn_sha256(args, vm):
        try:
            h = hashlib.sha256(args[0].to_python().encode()).hexdigest()
            return create_string(vm, h)
        except Exception:
            return NullValue()
            
    def fn_random_hex(args, vm):
        try:
            length = int(args[0].value)
            return create_string(vm, secrets.token_hex(length))
        except Exception:
            return create_string(vm, secrets.token_hex(16))

    registry.register("crypto::sha256", fn_sha256)
    registry.register("crypto::random_hex", fn_random_hex)
