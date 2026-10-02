# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import os
import json
import base64
import hmac
import hashlib
import time

_DEVELOPMENT_SECRET = b"aayu-development-only-secret"


def get_jwt_secret(require_configured: bool = False) -> bytes:
    """Return the configured signing secret without shipping a production secret."""
    configured = os.environ.get("AAYU_JWT_SECRET")
    if configured:
        if len(configured) < 32:
            raise RuntimeError("AAYU_JWT_SECRET must contain at least 32 characters")
        return configured.encode("utf-8")
    if require_configured:
        raise RuntimeError("AAYU_JWT_SECRET is required in production mode")
    return _DEVELOPMENT_SECRET


def mint_jwt(payload: dict, secret: bytes = None) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    
    # Add expiration (default 24h)
    if "exp" not in payload:
        payload["exp"] = int(time.time()) + 86400
        
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    signature = hmac.new(secret or get_jwt_secret(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token: str, secret: bytes = None) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        return None
        
    header_b64, payload_b64, signature_b64 = parts
    
    expected_sig = hmac.new(secret or get_jwt_secret(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
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
                }, secret=get_jwt_secret(not getattr(vm.config, "debug_mode", False)))
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
            }, secret=get_jwt_secret(not getattr(vm.config, "debug_mode", False)))
            if vm.state_scopes:
                vm.state_scopes[-1]["authToken"] = token
            vm.state["authToken"] = token
            return token
            
        return None

    registry.register("auth.register", auth_register)
    registry.register("auth.login", auth_login)
