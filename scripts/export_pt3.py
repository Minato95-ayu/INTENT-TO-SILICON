import os

filepath_init = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\__init__.py'
with open(filepath_init, 'r', encoding='utf-8') as f:
    content = f.read()

content += '''
from .logging_lib import register_logging_lib
from .testing_lib import register_testing_lib
from .compression_lib import register_compression_lib
from .concurrency_lib import register_concurrency_lib
'''
with open(filepath_init, 'w', encoding='utf-8') as f:
    f.write(content)

filepath_stdlib = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\stdlib.py'
with open(filepath_stdlib, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('register_process_lib', 'register_process_lib, register_logging_lib, register_testing_lib, register_compression_lib, register_concurrency_lib')

content = content.replace('register_process_lib(self.registry)', 'register_process_lib(self.registry)\n        register_logging_lib(self.registry)\n        register_testing_lib(self.registry)\n        register_compression_lib(self.registry)\n        register_concurrency_lib(self.registry)')

with open(filepath_stdlib, 'w', encoding='utf-8') as f:
    f.write(content)

print("Exported remaining libs")
