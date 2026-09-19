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

with open("runtime/stdlib/modules/http_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

new_func = '''def register_http_lib(registry):
    registry.register('HTTP.get', http_get)
    registry.register('HTTP.post', http_post)
    registry.register('http::get', http_get)
    registry.register('http::post', http_post)
'''
content = content.replace('def register_http_lib(registry):\n    registry.register(\'HTTP.get\', http_get)\n    registry.register(\'HTTP.post\', http_post)\n', new_func)

with open("runtime/stdlib/modules/http_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated http_lib")
