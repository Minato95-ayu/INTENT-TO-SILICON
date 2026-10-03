import sys

def patch():
    with open("compiler/ir/linearizer.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = """        elif isinstance(term, Return):
            if term.value is not None:
                self._push_value(term.value)
                self._emit("RETURN_VALUE", [])
            else:
                self._emit("RET", [])"""
                
    new_target = """        elif isinstance(term, Return):
            if term.value is not None:
                self._push_value(term.value)
                self._emit("RETURN_VALUE", [])
            else:
                # Force void actions to return null to satisfy CALL_ACTION expecting 1 return
                self._push_value(None)
                self._emit("RETURN_VALUE", [])"""

    if target in content:
        content = content.replace(target, new_target)
        with open("compiler/ir/linearizer.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched linearizer.py!")
    else:
        print("Target not found in linearizer.py")

patch()
