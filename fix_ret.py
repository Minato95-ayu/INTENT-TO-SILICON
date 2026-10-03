import re

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    content = f.read()

def replace_ret(content):
    old_unpack = "ret_ip, is_comp, expected_returns, args, base_depth = self.vm.call_stack.pop()"
    new_unpack = """
            frame = self.vm.call_stack.pop()
            if len(frame) == 6:
                ret_ip, is_comp, expected_returns, args, base_depth, base_scope_depth = frame
            else:
                ret_ip, is_comp, expected_returns, args, base_depth = frame
                base_scope_depth = 0
"""
    content = content.replace(old_unpack, new_unpack)
    
    old_scope = """            if hasattr(self.vm, 'state_scopes') and len(self.vm.state_scopes) > 1:
                self.vm.state_scopes.pop()"""
    new_scope = """            if hasattr(self.vm, 'state_scopes') and len(self.vm.state_scopes) > 1:
                self.vm.state_scopes.pop()
            if hasattr(self.vm, 'state') and hasattr(self.vm.state, 'scopes'):
                while len(self.vm.state.scopes) > base_scope_depth:
                    self.vm.state.scopes.pop()"""
    content = content.replace(old_scope, new_scope)
    return content

content = replace_ret(content)

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(content)
