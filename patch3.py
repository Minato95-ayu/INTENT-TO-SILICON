import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "async def asgi_app(self, scope, receive, send):\n        try:",
    "async def asgi_app(self, scope, receive, send):\n        print('ENTERED ASGI APP!', flush=True)\n        try:"
)
with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)