import urllib.request
import urllib.error
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def register_http_lib(registry: StdLibRegistry):
    def fn_get(args, vm):
        try:
            req = urllib.request.Request(args[0].to_python(), headers={'User-Agent': 'AAYU/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return create_string(vm, response.read().decode('utf-8'))
        except Exception:
            return NullValue()
            
    def fn_post(args, vm):
        try:
            url = args[0].to_python()
            data = args[1].to_python().encode('utf-8') if len(args) > 1 else b""
            req = urllib.request.Request(url, data=data, headers={'User-Agent': 'AAYU/1.0', 'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                return create_string(vm, response.read().decode('utf-8'))
        except Exception:
            return NullValue()
            
    registry.register("http::get", fn_get)
    registry.register("http::post", fn_post)
