import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\stdlib.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('register_http_lib, register_crypto_lib, register_core_lib',
                          'register_http_lib, register_crypto_lib, register_core_lib, register_database_lib, register_regex_lib, register_env_lib, register_process_lib')

content = content.replace('register_random_lib(self.registry)',
                          'register_random_lib(self.registry)\n        register_database_lib(self.registry)\n        register_regex_lib(self.registry)\n        register_env_lib(self.registry)\n        register_process_lib(self.registry)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated stdlib.py")
