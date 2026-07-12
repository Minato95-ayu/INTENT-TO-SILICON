import urllib.request
import urllib.error
import socket
import ssl
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue

def create_string(vm, text):
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def register_http_lib(registry: StdLibRegistry):
    def handle_request(req, vm, timeout=10):
        try:
            # Create a context that handles SSL reasonably well
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                return create_string(vm, response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return create_string(vm, f"HTTPError: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if "CERTIFICATE_VERIFY_FAILED" in reason:
                return create_string(vm, "error: SSL failure")
            elif "No address associated with hostname" in reason or "getaddrinfo failed" in reason:
                return create_string(vm, "error: DNS failure or invalid hostname")
            elif "Connection refused" in reason:
                return create_string(vm, "error: connection refused")
            return create_string(vm, f"URLError: {reason}")
        except socket.timeout:
            return create_string(vm, "error: timeout")
        except Exception as e:
            return create_string(vm, f"error: {str(e)}")

    def fn_get(args, vm):
        url = args[0].to_python()
        timeout = 10
        if len(args) > 1:
            timeout = args[1].to_python()
            
        req = urllib.request.Request(url, headers={'User-Agent': 'AAYU/1.0'})
        return handle_request(req, vm, timeout)
            
    def fn_post(args, vm):
        url = args[0].to_python()
        data = args[1].to_python().encode('utf-8') if len(args) > 1 else b""
        timeout = 10
        if len(args) > 2:
            timeout = args[2].to_python()
            
        req = urllib.request.Request(url, data=data, headers={'User-Agent': 'AAYU/1.0', 'Content-Type': 'application/json'}, method='POST')
        return handle_request(req, vm, timeout)
            
    registry.register("http::get", fn_get)
    registry.register("http::post", fn_post)
