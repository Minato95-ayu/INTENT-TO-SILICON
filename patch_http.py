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
