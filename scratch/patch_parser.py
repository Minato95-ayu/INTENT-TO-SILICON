import re

with open("aayu/compiler/parser/parser.py", "r") as f:
    content = f.read()

# Fix _parse_action_call property access
old_action_call = """
        while self._match(TokenType.SYMBOL, "."):
            if not (self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD)):
                raise CompilerError(f"Expect property name after '.', got {self._peek().value}", self._peek().line, self._peek().column)
            prop = self._advance().value
            name = f"{name}.{prop}"
"""
new_action_call = """
        while self._check(TokenType.SYMBOL, ".") and self.pos + 1 < self.length and self.tokens[self.pos].line == self.tokens[self.pos+1].line:
            if not (self.tokens[self.pos+1].type == TokenType.IDENTIFIER or self.tokens[self.pos+1].type == TokenType.KEYWORD):
                break
            self._advance() # consume .
            prop = self._advance().value
            name = f"{name}.{prop}"
"""
if old_action_call in content:
    content = content.replace(old_action_call, new_action_call)
else:
    print("WARNING: action_call match failed")

# Fix _parse_primary lookahead for `is_call`
old_lookahead = """
            while self.pos + lookahead < self.length:
                if self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == "(":
                    is_call = True
                    break
                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    lookahead += 2
                else:
                    break
"""
new_lookahead = """
            while self.pos + lookahead < self.length:
                if self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == "(":
                    is_call = True
                    break
                elif self.tokens[self.pos+lookahead].type == TokenType.SYMBOL and self.tokens[self.pos+lookahead].value == ".":
                    if self.pos + lookahead + 1 < self.length and self.tokens[self.pos+lookahead].line == self.tokens[self.pos+lookahead+1].line:
                        lookahead += 2
                    else:
                        break
                else:
                    break
"""
if old_lookahead in content:
    content = content.replace(old_lookahead, new_lookahead)
else:
    print("WARNING: lookahead match failed")

with open("aayu/compiler/parser/parser.py", "w") as f:
    f.write(content)
print("Patched parser property access.")
