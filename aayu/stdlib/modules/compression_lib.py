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
