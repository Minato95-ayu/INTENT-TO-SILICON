import os

crypto_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\crypto_lib.py'
with open(crypto_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = """\
from ..helpers import make_string, make_list, make_map
from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.boolean import BooleanValue
import hashlib
import uuid
import base64
import os as _os
import bcrypt

def register_crypto_lib(registry: StdLibRegistry):
    def fn_sha256(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return make_string(vm, hashlib.sha256(s.encode('utf-8')).hexdigest())
    registry.register("crypto::sha256", fn_sha256)
    
    def fn_md5(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return make_string(vm, hashlib.md5(s.encode('utf-8')).hexdigest())
    registry.register("crypto::md5", fn_md5)
    
    def fn_uuid(args, vm):
        return make_string(vm, str(uuid.uuid4()))
    registry.register("crypto::uuid", fn_uuid)

    def fn_base64_encode(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        return make_string(vm, base64.b64encode(s.encode('utf-8')).decode('utf-8'))
    registry.register("crypto::base64_encode", fn_base64_encode)
    
    def fn_base64_decode(args, vm):
        if not args: return NullValue()
        s = args[0].to_python()
        try:
            return make_string(vm, base64.b64decode(s.encode('utf-8')).decode('utf-8'))
        except:
            return NullValue()
    registry.register("crypto::base64_decode", fn_base64_decode)
    
    def fn_bcrypt_hash(args, vm):
        if not args: return NullValue()
        password = args[0].to_python().encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return make_string(vm, hashed.decode('utf-8'))
    registry.register("crypto::bcrypt_hash", fn_bcrypt_hash)
    
    def fn_bcrypt_verify(args, vm):
        if len(args) < 2: return BooleanValue(False)
        stored_hash = args[0].to_python().encode('utf-8')
        password = args[1].to_python().encode('utf-8')
        try:
            return BooleanValue(bcrypt.checkpw(password, stored_hash))
        except:
            return BooleanValue(False)
    registry.register("crypto::bcrypt_verify", fn_bcrypt_verify)
"""

with open(crypto_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed crypto_lib.py")
