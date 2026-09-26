import os
import sys

wr_path = 'runtime/renderers/web_renderer.py'
with open(wr_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'kwargs={"host": "0.0.0.0", "port": self.port, "log_level": "trace"},',
    'kwargs={"host": "0.0.0.0", "port": self.port, "log_level": "error"},'
)

with open(wr_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("PATCHED log_level")