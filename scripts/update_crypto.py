import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\crypto_lib.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import uuid\n', 'import uuid\nimport base64\nimport os as _os\nimport hmac\n')

bcrypt_impl = """
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
        # Mocking bcrypt using pbkdf2 to keep AAYU dependency-free
        password = args[0].to_python().encode()
        salt = _os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
        return make_string(vm, f"{salt.hex()}:{hashed.hex()}")
    registry.register("crypto::bcrypt_hash", fn_bcrypt_hash)
    
    def fn_bcrypt_verify(args, vm):
        if len(args) < 2: return BooleanValue(False)
        stored_hash = args[0].to_python()
        password = args[1].to_python().encode()
        if ':' not in stored_hash: return BooleanValue(False)
        try:
            salt_hex, hash_hex = stored_hash.split(':', 1)
            salt = bytes.fromhex(salt_hex)
            hashed = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
            return BooleanValue(hmac.compare_digest(hashed.hex(), hash_hex))
        except:
            return BooleanValue(False)
    registry.register("crypto::bcrypt_verify", fn_bcrypt_verify)
"""

content = content.replace('registry.register("crypto::uuid", fn_uuid)', 'registry.register("crypto::uuid", fn_uuid)\n' + bcrypt_impl)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated crypto_lib.py")
