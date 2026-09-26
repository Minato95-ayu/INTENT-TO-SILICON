import os
import sys

# Patch LSP log
for fpath in ['tools/aayu_lsp.py', 'tools/lsp/server.py']:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            code = f.read()
        code = code.replace(
            "filename='aayu_lsp.log'",
            "filename=__import__('os').path.join(__import__('tempfile').gettempdir(), 'aayu_lsp.log')"
        )
        code = code.replace(
            'filename="aayu_lsp.log"',
            "filename=__import__('os').path.join(__import__('tempfile').gettempdir(), 'aayu_lsp.log')"
        )
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)

# Patch web renderer build dir
wr_path = 'runtime/renderers/web_renderer.py'
with open(wr_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'self.build_dir = os.path.join(self.project_dir, ".aayu", "build")',
    'self.build_dir = os.path.join(__import__("tempfile").gettempdir(), "aayu_web_build")'
)

with open(wr_path, 'w', encoding='utf-8') as f:
    f.write(code)

# Suppress PAGE_START error
vm_path = 'runtime/vm/interpreter.py'
with open(vm_path, 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace(
    "print(f\"[VM] Error: Action '{func_name}' not found.\")",
    "if func_name != '__PAGE_START__': print(f\"[VM] Error: Action '{func_name}' not found.\")"
)
with open(vm_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("PATCHED ALL")