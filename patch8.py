import sys
with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'renderer.start()' in code and 'print("🚀 Starting AAYU Web Server' not in code:
    code = code.replace(
        'renderer.start()',
        'print(f"\n🚀 Starting AAYU Web Server at http://localhost:{port} ...", flush=True)\n            renderer.start()'
    )
    with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
        f.write(code)