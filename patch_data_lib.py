# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re

with open("runtime/stdlib/modules/__init__.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from .ml import *", "from .ml import *\nfrom .data_lib import register_data_lib")
# if it doesn't exist, just append
if "from .data_lib import" not in content:
    content += "\nfrom .data_lib import register_data_lib\n"

with open("runtime/stdlib/modules/__init__.py", "w", encoding="utf-8") as f:
    f.write(content)

with open("runtime/stdlib/stdlib.py", "r", encoding="utf-8") as f:
    content2 = f.read()

content2 = content2.replace("register_storage_lib, register_auth_lib", "register_storage_lib, register_auth_lib, register_data_lib")
content2 = content2.replace("register_ai_lib(self.registry)", "register_ai_lib(self.registry)\n        register_data_lib(self.registry)")

with open("runtime/stdlib/stdlib.py", "w", encoding="utf-8") as f:
    f.write(content2)

print("data_lib registered")
