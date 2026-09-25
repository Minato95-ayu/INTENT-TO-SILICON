import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Make sure to replace the arguments to the thread
code = code.replace(
    "args=(self.asgi_app,),",
    "args=(asgi_wrapper,),"
)

code = code.replace(
    "def uvicorn_run(*args, **kwargs):",
    "async def asgi_wrapper(scope, receive, send):\n            await self.asgi_app(scope, receive, send)\n\n        def uvicorn_run(*args, **kwargs):"
)

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)