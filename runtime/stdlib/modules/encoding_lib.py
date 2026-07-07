from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
import base64

def register_encoding_lib(registry: StdLibRegistry):
    def fn_base64_encode(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return make_string(vm, base64.b64encode(s.encode('utf-8')).decode('utf-8'))
    registry.register("encoding::base64_encode", fn_base64_encode)
