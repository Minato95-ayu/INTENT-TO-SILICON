from runtime.http.middleware import MiddlewareBase

class SecurityMiddleware(MiddlewareBase):
    def process(self, ctx):
        # Apply standard sane defaults for AAYU Native Runtime
        ctx.response.set_header("X-Powered-By", "AAYU Runtime")
        ctx.response.set_header("X-Content-Type-Options", "nosniff")
        ctx.response.set_header("X-Frame-Options", "DENY")
        ctx.response.set_header("X-XSS-Protection", "1; mode=block")
        
        # In a real environment, we would also process CORS and CSRF tokens here
