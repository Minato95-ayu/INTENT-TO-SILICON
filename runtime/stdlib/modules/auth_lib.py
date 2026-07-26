import os
import json
import base64
import hmac
import hashlib
import time

# Simple V1 JWT Secret (Zero-dependency)
JWT_SECRET = b"aayu_super_secret_v1"

def mint_jwt(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    
    # Add expiration (default 24h)
    if "exp" not in payload:
        payload["exp"] = int(time.time()) + 86400
        
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    signature = hmac.new(JWT_SECRET, f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        return None
        
    header_b64, payload_b64, signature_b64 = parts
    
    expected_sig = hmac.new(JWT_SECRET, f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")
    
    if not hmac.compare_digest(signature_b64, expected_sig_b64):
        return None
        
    # Pad payload
    padding = "=" * (4 - (len(payload_b64) % 4))
    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + padding).decode())
    
    if payload.get("exp", 0) < time.time():
        return None # Expired
        
    return payload

def register_auth_lib(registry):
    def auth_register(args, vm):
        # We assume the implicit aayu_auth_user table or dynamic table
        vm.database.execute_query("""
            CREATE TABLE IF NOT EXISTS aayu_auth_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password_hash TEXT,
                roles TEXT DEFAULT '[]',
                permissions TEXT DEFAULT '[]'
            )
        """)
        
        email = args[0]
        password = args[1]
        print(f"[AUTH] Registering {email}...")
        
        from runtime.stdlib.stdlib import hash_password
        pwd_hash = hash_password(password)
        
        try:
            vm.database.execute_query(
                "INSERT INTO aayu_auth_user (email, password_hash) VALUES (?, ?)",
                (email, pwd_hash)
            )
            # Fetch id
            user = vm.database.execute_query("SELECT id, roles, permissions FROM aayu_auth_user WHERE email = ?", (email,))
            if user:
                token = mint_jwt({
                    "id": user[0]["id"], 
                    "email": email,
                    "roles": json.loads(user[0]["roles"]),
                    "permissions": json.loads(user[0]["permissions"])
                })
                # Inject directly into state
                if vm.state_scopes:
                    vm.state_scopes[-1]["authToken"] = token
                vm.state["authToken"] = token
                return token
        except Exception as e:
            print(f"[AUTH] Exception in register: {e}")
            return ""
        return ""

    def auth_login(args, vm):
        email = args[0]
        password = args[1]
        
        try:
            user = vm.database.execute_query("SELECT * FROM aayu_auth_user WHERE email = ?", (email,))
        except Exception:
            return ""
            
        if not user:
            return None
            
        stored_hash = user[0]["password_hash"]
        from runtime.stdlib.stdlib import verify_password
        
        if verify_password(stored_hash, password):
            token = mint_jwt({
                "id": user[0]["id"], 
                "email": email,
                "roles": json.loads(user[0].get("roles", "[]")),
                "permissions": json.loads(user[0].get("permissions", "[]"))
            })
            if vm.state_scopes:
                vm.state_scopes[-1]["authToken"] = token
            vm.state["authToken"] = token
            return token
            
        return None

    registry.register("auth.register", auth_register)
    registry.register("auth.login", auth_login)
