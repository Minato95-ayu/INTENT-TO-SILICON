import sys

with open('runtime/vm/database.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_code = '''        if decorators:
            for dec in decorators:
                if dec.name == 'Secure':
                    is_secure = True
                    for arg in dec.args:
                        if hasattr(arg, 'name') and arg.name == 'roles':
                            if hasattr(arg, 'value') and isinstance(arg.value, list):
                                roles = [v.value for v in arg.value]
                            elif isinstance(arg.value, list):
                                roles = arg.value
                        elif isinstance(arg, dict) and 'roles' in arg:
                            roles = arg['roles']
                        elif hasattr(arg, 'name') and arg.name == 'permissions':
                            if hasattr(arg, 'value') and isinstance(arg.value, list):
                                permissions = [v.value for v in arg.value]
                        elif isinstance(arg, dict) and 'permissions' in arg:
                            permissions = arg['permissions']
                        elif hasattr(arg, 'name') and arg.name == 'owner' and (arg.value is True):
                            is_owner = True
                        elif isinstance(arg, dict) and arg.get('owner') is True:
                            is_owner = True
                elif dec.name == 'SoftDelete':
                    is_soft_delete = True'''

new_code = '''        if decorators:
            for dec in decorators:
                if isinstance(dec, dict):
                    name = dec.get('name')
                    args = dec.get('args', [])
                else:
                    name = getattr(dec, 'name', None)
                    args = getattr(dec, 'args', [])
                    
                if name == 'Secure':
                    is_secure = True
                    for arg in args:
                        arg_name = arg.get('name') if isinstance(arg, dict) else getattr(arg, 'name', None)
                        arg_value = arg.get('value') if isinstance(arg, dict) else getattr(arg, 'value', None)
                        
                        if arg_name == 'roles' and isinstance(arg_value, list):
                            roles = [v.get('value', v) if isinstance(v, dict) else getattr(v, 'value', v) for v in arg_value]
                        elif arg_name == 'permissions' and isinstance(arg_value, list):
                            permissions = [v.get('value', v) if isinstance(v, dict) else getattr(v, 'value', v) for v in arg_value]
                        elif arg_name == 'owner' and arg_value is True:
                            is_owner = True
                elif name == 'Owner':
                    is_owner = True
                elif name == 'SoftDelete':
                    is_soft_delete = True'''

if old_code in code:
    code = code.replace(old_code, new_code)
    with open('runtime/vm/database.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("PATCH SUCCESSFUL")
else:
    print("COULD NOT FIND OLD CODE TO PATCH")