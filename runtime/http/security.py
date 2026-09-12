"""
AAYU Runtime — Security Headers Middleware
Applies OWASP-recommended security headers to all HTTP responses.
CORS and CSRF are handled by dedicated middleware in cors.py.
"""

from runtime.http.middleware import MiddlewareBase


class SecurityMiddleware(MiddlewareBase):
    """
    Production-grade security headers middleware for the AAYU HTTP engine.

    Applies OWASP-recommended response headers to harden against:
    - MIME sniffing attacks (X-Content-Type-Options)
    - Clickjacking (X-Frame-Options, CSP frame-ancestors)
    - Cross-site scripting (Content-Security-Policy)
    - Information leakage (Referrer-Policy, Permissions-Policy)
    - Insecure transport (Strict-Transport-Security when TLS enabled)

    All headers can be overridden via constructor arguments.
    """

    def __init__(
        self,
        tls_enabled=False,
        hsts_max_age=31536000,
        csp_directives=None,
        permissions_policy=None,
    ):
        self.tls_enabled = tls_enabled
        self.hsts_max_age = hsts_max_age

        # Default Content-Security-Policy — strict by default
        self.csp = csp_directives or {
            "default-src": "'none'",
            "script-src": "'self'",
            "style-src": "'self' 'unsafe-inline'",
            "img-src": "'self' data:",
            "font-src": "'self'",
            "connect-src": "'self'",
            "frame-ancestors": "'none'",
            "base-uri": "'self'",
            "form-action": "'self'",
        }

        # Default Permissions-Policy — deny sensitive APIs
        self.permissions_policy = permissions_policy or {
            "camera": "()",
            "microphone": "()",
            "geolocation": "()",
            "payment": "()",
            "usb": "()",
        }

    def _build_csp_header(self):
        """Build the Content-Security-Policy header value from directives dict."""
        return "; ".join(
            f"{directive} {value}" for directive, value in self.csp.items()
        )

    def _build_permissions_policy(self):
        """Build the Permissions-Policy header value from policy dict."""
        return ", ".join(
            f"{feature}={value}" for feature, value in self.permissions_policy.items()
        )

    def process(self, ctx):
        # Server identification — intentionally vague for security
        ctx.response.set_header("X-Powered-By", "AAYU Runtime")

        # Prevent MIME sniffing (OWASP)
        ctx.response.set_header("X-Content-Type-Options", "nosniff")

        # Prevent clickjacking (OWASP)
        ctx.response.set_header("X-Frame-Options", "DENY")

        # XSS protection — modern browsers use CSP, but this is defense-in-depth
        ctx.response.set_header("X-XSS-Protection", "1; mode=block")

        # Referrer policy — prevent leaking URLs to third parties
        ctx.response.set_header("Referrer-Policy", "strict-origin-when-cross-origin")

        # Content-Security-Policy — primary XSS and injection defense
        ctx.response.set_header("Content-Security-Policy", self._build_csp_header())

        # Permissions-Policy — restrict browser feature access
        ctx.response.set_header("Permissions-Policy", self._build_permissions_policy())

        # Cache control — prevent caching of sensitive responses
        ctx.response.set_header("Cache-Control", "no-store, no-cache, must-revalidate")

        # Strict Transport Security — only set when TLS is active
        if self.tls_enabled:
            ctx.response.set_header(
                "Strict-Transport-Security",
                f"max-age={self.hsts_max_age}; includeSubDomains"
            )

