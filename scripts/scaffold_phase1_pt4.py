import os

runtime_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules"

def write_file(path, content):
    with open(os.path.join(runtime_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

write_file("networking_lib.py", """\
from ..helpers import make_string
from ..registry import StdLibRegistry
from ...values.null import NullValue
from ...values.boolean import BooleanValue
import socket

def register_networking_lib(registry: StdLibRegistry):
    def fn_ping(args, vm):
        if not args: return BooleanValue(False)
        host = args[0].to_python()
        try:
            # Simple connect test
            s = socket.create_connection((host, 80), 2)
            s.close()
            return BooleanValue(True)
        except:
            return BooleanValue(False)
    registry.register("networking::ping", fn_ping)
""")

write_file("encoding_lib.py", """\
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
""")

filepath_init = os.path.join(runtime_dir, '__init__.py')
with open(filepath_init, 'a', encoding='utf-8') as f:
    f.write('''
from .networking_lib import register_networking_lib
from .encoding_lib import register_encoding_lib
''')

filepath_stdlib = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\stdlib.py'
with open(filepath_stdlib, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('register_concurrency_lib', 'register_concurrency_lib, register_networking_lib, register_encoding_lib')

content = content.replace('register_concurrency_lib(self.registry)', 'register_concurrency_lib(self.registry)\n        register_networking_lib(self.registry)\n        register_encoding_lib(self.registry)')

with open(filepath_stdlib, 'w', encoding='utf-8') as f:
    f.write(content)

print("Created networking and encoding libs")
