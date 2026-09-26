import sys

with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_code = '''        if renderer:
            renderer.initialize()'''

new_code = '''        if renderer:
            renderer.initialize()
            if hasattr(renderer, 'start'):
                print(f"\\n🚀 Starting AAYU Web Server at http://localhost:{port} ...", flush=True)
                renderer.start()'''

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("PATCH SUCCESSFUL")
else:
    print("COULD NOT FIND OLD CODE TO PATCH")