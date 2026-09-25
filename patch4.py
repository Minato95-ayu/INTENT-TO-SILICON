import sys
with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "config = uvicorn.Config(*args, **kwargs)",
    "import sys\n            sys.stderr = open('uvicorn_stderr.log', 'w')\n            config = uvicorn.Config(*args, **kwargs)"
)
with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)