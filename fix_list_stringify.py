with open("runtime/values/list.py", "r", encoding="utf-8") as f:
    content = f.read()

old_stringify = """    def stringify(self) -> str:
        return str(self.to_python())"""

new_stringify = """    def stringify(self) -> str:
        elements = self._get_payload()
        stringified = []
        for e in elements:
            if hasattr(e, "stringify"):
                stringified.append(e.stringify())
            elif hasattr(e, "to_python"):
                stringified.append(repr(e.to_python()))
            else:
                stringified.append(repr(e))
        return "[" + ", ".join(stringified) + "]" """

if old_stringify in content:
    content = content.replace(old_stringify, new_stringify)
    with open("runtime/values/list.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed list stringify")
else:
    print("Code not found")
