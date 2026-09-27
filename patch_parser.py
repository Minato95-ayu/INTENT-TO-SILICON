with open("compiler/parser/parser.py", "r", encoding="utf-8") as f:
    content = f.read()

old_code = '''                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    has_dot = True
                    lookahead += 2
                else:'''

new_code = '''                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    has_dot = True
                    lookahead += 2
                elif self.tokens[self.pos+lookahead].type == TokenType.OPERATOR and self.tokens[self.pos+lookahead].value == "::":
                    lookahead += 2
                else:'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("compiler/parser/parser.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched parser successfully.")
else:
    print("Code not found.")
