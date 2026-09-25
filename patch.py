import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "async def asgi_app(self, scope, receive, send):",
    "async def asgi_app(self, scope, receive, send):\n        try:\n            await self._asgi_app_inner(scope, receive, send)\n        except Exception as e:\n            import traceback\n            traceback.print_exc()\n            raise\n\n    async def _asgi_app_inner(self, scope, receive, send):"
)
with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)