import sys

with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'print(f"\\n🚀 Starting AAYU Web Server at http://localhost:{port} ...", flush=True)',
    'print(f"\\n>> Starting AAYU Web Server at http://localhost:{port} ...", flush=True)'
)
with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCH SUCCESSFUL")