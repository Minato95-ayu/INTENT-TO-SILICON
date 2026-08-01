with open('compiler/bytecode/constant_pool.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''        type_tag = self._infer_type(value)
        key = (type_tag, value)

        if key in self._index_cache:'''

new_code = '''        type_tag = self._infer_type(value)
        if isinstance(value, dict):
            key_val = str(sorted([(k, str(v)) for k, v in value.items()]))
        else:
            key_val = value
        key = (type_tag, key_val)

        if key in self._index_cache:'''

content = content.replace(old_code, new_code)

old_infer = '''        elif isinstance(value, str):
            return "STRING"
        else:
            return "STRING"  # fallback: serialize as string'''

new_infer = '''        elif isinstance(value, str):
            return "STRING"
        elif isinstance(value, dict):
            return "DICT"
        else:
            return "STRING"  # fallback: serialize as string'''
            
content = content.replace(old_infer, new_infer)

with open('compiler/bytecode/constant_pool.py', 'w', encoding='utf-8') as f:
    f.write(content)
