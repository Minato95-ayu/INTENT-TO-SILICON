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

"""
AAYU Runtime — CORS Middleware
Handles Cross-Origin Resource Sharing (CORS) for the AAYU HTTP engine.
Provides configurable origin whitelisting, methods, headers, and preflight handling.
"""

import time
import secrets
from runtime.http.middleware import MiddlewareBase


class CORSMiddleware(MiddlewareBase):
    """
    Production-grade CORS middleware for the AAYU HTTP pipeline.

    Handles:
    - Origin whitelisting (specific origins or wildcard for dev)
    - Preflight OPTIONS requests with proper Access-Control headers
    - Configurable allowed methods and headers
    - Max-age caching for preflight results
    - Credentials support
    """

    def __init__(
        self,
        allowed_origins=None,
        allowed_methods=None,
        allowed_headers=None,
        expose_headers=None,
        allow_credentials=False,
        max_age=86400,
    ):
        # Default: no wildcard in production — must explicitly configure origins
        self.allowed_origins = set(allowed_origins or [])
        self.allowed_methods = set(allowed_methods or {
            "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
        })
        self.allowed_headers = set(allowed_headers or {
            "Content-Type", "Authorization", "X-Request-ID", "Accept"
        })
        self.expose_headers = set(expose_headers or {
            "X-Request-ID", "X-RateLimit-Remaining"
        })
        self.allow_credentials = allow_credentials
        self.max_age = max_age

    def _origin_allowed(self, origin):
        """Check if the request origin is in the whitelist."""
        if not origin:
            return False
        if "*" in self.allowed_origins:
            return True
        return origin in self.allowed_origins

    def process(self, ctx):
        origin = ctx.request.headers.get("Origin", "")

        if not self._origin_allowed(origin):
            # If origin is not allowed, do NOT set any CORS headers.
            # The browser will block the response on the client side.
            return

        # Set CORS response headers for allowed origins
        ctx.response.set_header("Access-Control-Allow-Origin", origin)

        if self.allow_credentials:
            ctx.response.set_header("Access-Control-Allow-Credentials", "true")

        ctx.response.set_header(
            "Access-Control-Expose-Headers",
            ", ".join(sorted(self.expose_headers))
        )

        # Handle preflight requests (OPTIONS method)
        if ctx.request.method == "OPTIONS":
            ctx.response.set_header(
                "Access-Control-Allow-Methods",
                ", ".join(sorted(self.allowed_methods))
            )
            ctx.response.set_header(
                "Access-Control-Allow-Headers",
                ", ".join(sorted(self.allowed_headers))
            )
            ctx.response.set_header(
                "Access-Control-Max-Age",
                str(self.max_age)
            )
            # Short-circuit: send 204 No Content for preflight
            ctx.response.status(204)
            ctx.response._send("text/plain", b"")


class CSRFMiddleware(MiddlewareBase):
    """
    CSRF protection middleware using double-submit cookie pattern.

    For state-changing methods (POST, PUT, PATCH, DELETE):
    - Validates that X-CSRF-Token header matches the csrf_token cookie
    - Generates a new CSRF token on GET requests if none exists

    Safe methods (GET, HEAD, OPTIONS) are always allowed through.
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
    TOKEN_HEADER = "X-CSRF-Token"
    TOKEN_COOKIE = "csrf_token"

    def __init__(self, enabled=True):
        self.enabled = enabled

    def _generate_token(self):
        """Generate a cryptographically secure CSRF token."""
        return secrets.token_hex(32)

    def process(self, ctx):
        if not self.enabled:
            return

        method = ctx.request.method.upper()

        # For safe methods: ensure a CSRF cookie exists for subsequent forms
        if method in self.SAFE_METHODS:
            if self.TOKEN_COOKIE not in ctx.request.cookies:
                token = self._generate_token()
                ctx.response.set_header(
                    "Set-Cookie",
                    f"{self.TOKEN_COOKIE}={token}; Path=/; HttpOnly; SameSite=Strict"
                )
                ctx.state["csrf_token"] = token
            return

        # For state-changing methods: validate the token
        cookie_token = ctx.request.cookies.get(self.TOKEN_COOKIE, "")
        header_token = ctx.request.headers.get(self.TOKEN_HEADER, "")

        if not cookie_token or not header_token:
            ctx.response.status(403).json({
                "error": "CSRF token missing",
                "message": "Include X-CSRF-Token header matching csrf_token cookie"
            })
            return

        if not secrets.compare_digest(cookie_token, header_token):
            ctx.response.status(403).json({
                "error": "CSRF token mismatch",
                "message": "X-CSRF-Token header does not match csrf_token cookie"
            })
            return


class AuthMiddleware(MiddlewareBase):
    """
    JWT Authentication middleware for the AAYU HTTP pipeline.

    Extracts Bearer token from Authorization header, validates it using
    the AAYU auth library, and injects the decoded user context into
    ctx.state["user"] for downstream handlers and RBAC middleware.

    Routes can be exempted from auth by adding their paths to `exempt_paths`.
    """

    def __init__(self, exempt_paths=None, require_in_production=True):
        self.exempt_paths = set(exempt_paths or {
            "/", "/health", "/openapi.json", "/docs", "/redoc"
        })
        self.require_in_production = require_in_production

    def process(self, ctx):
        # Skip auth for exempt paths
        if ctx.request.path in self.exempt_paths:
            return

        # Skip OPTIONS preflight (CORS handles it)
        if ctx.request.method == "OPTIONS":
            return

        auth_header = ctx.request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            ctx.response.status(401).json({
                "error": "Authentication required",
                "message": "Provide Authorization: Bearer <token> header"
            })
            return

        token = auth_header[7:].strip()
        if not token:
            ctx.response.status(401).json({
                "error": "Empty token",
                "message": "Bearer token cannot be empty"
            })
            return

        # Validate JWT using AAYU's auth library
        from runtime.stdlib.modules.auth_lib import verify_jwt
        payload = verify_jwt(token)

        if payload is None:
            ctx.response.status(401).json({
                "error": "Invalid or expired token",
                "message": "Token verification failed — check expiry and signature"
            })
            return

        # Inject authenticated user context for downstream handlers
        ctx.state["user"] = payload
        ctx.state["user_id"] = payload.get("id")
        ctx.state["user_roles"] = payload.get("roles", [])
        ctx.state["user_permissions"] = payload.get("permissions", [])


class RBACMiddleware(MiddlewareBase):
    """
    Role-Based Access Control middleware for the AAYU HTTP pipeline.

    Checks route-level role/permission requirements against the authenticated
    user context (populated by AuthMiddleware).

    Route requirements are configured via a role_map:
        {
            "/api/admin/users": {"roles": ["admin"], "permissions": []},
            "/api/reports": {"roles": ["admin", "manager"], "permissions": ["read_reports"]},
        }

    Admin role implicitly grants all access.
    """

    def __init__(self, role_map=None):
        self.role_map = role_map or {}

    def process(self, ctx):
        # Skip if no user context (AuthMiddleware didn't run or path was exempt)
        if "user" not in ctx.state:
            return

        # Check if this path has role/permission requirements
        requirements = self.role_map.get(ctx.request.path)
        if not requirements:
            return

        user_roles = ctx.state.get("user_roles", [])
        user_permissions = ctx.state.get("user_permissions", [])

        # Admin bypass — admin role implicitly grants all access
        if "admin" in user_roles:
            return

        # Check required roles
        required_roles = requirements.get("roles", [])
        if required_roles and not any(r in user_roles for r in required_roles):
            ctx.response.status(403).json({
                "error": "Forbidden",
                "message": f"Required role(s): {', '.join(required_roles)}"
            })
            return

        # Check required permissions
        required_perms = requirements.get("permissions", [])
        if required_perms and not any(p in user_permissions for p in required_perms):
            ctx.response.status(403).json({
                "error": "Forbidden",
                "message": f"Required permission(s): {', '.join(required_perms)}"
            })
            return
