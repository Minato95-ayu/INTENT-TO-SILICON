
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/parser/parser.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

old_code = """        if self._match(TokenType.IDENTIFIER, "page"):
            return self._parse_widget("Page")"""

new_code = """        if self._match(TokenType.IDENTIFIER, "page"):
            return self._parse_widget("Page")
            
        if self._match(TokenType.IDENTIFIER, "component"):
            return self._parse_widget("Component")"""

if old_code in c:
    c = c.replace(old_code, new_code)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched parser.py")
else:
    print("Could not find old code in parser.py")

