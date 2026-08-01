import re

with open("aayu/compiler/parser/parser.py", "r") as f:
    content = f.read()

# Refactor _parse_if_statement
old_if = """    def _parse_if_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        then_branch = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end") and not self._check(TokenType.KEYWORD, "else"):
            then_branch.append(self._parse_statement())
            
        else_branch = None
        if self._match(TokenType.KEYWORD, "else"):
            else_branch = []
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                else_branch.append(self._parse_statement())
                
        self._consume(TokenType.KEYWORD, "Expect 'end' after if statement.", value="end")
        from aayu.compiler.ast.nodes import IfNode
        return IfNode(line=line, column=col, condition=condition, then_branch=then_branch, else_branch=else_branch)"""

new_if = """    def _parse_if_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        
        has_brace = False
        if self._match(TokenType.SYMBOL, "{"):
            has_brace = True
            
        then_branch = []
        while not self._is_at_end():
            if has_brace and self._check(TokenType.SYMBOL, "}"):
                break
            if not has_brace and (self._check(TokenType.KEYWORD, "end") or self._check(TokenType.KEYWORD, "else")):
                break
            then_branch.append(self._parse_statement())
            
        if has_brace:
            self._consume(TokenType.SYMBOL, "Expect '}' after if block.", value="}")
            
        else_branch = None
        if self._match(TokenType.KEYWORD, "else"):
            has_else_brace = False
            if self._match(TokenType.SYMBOL, "{"):
                has_else_brace = True
                
            else_branch = []
            while not self._is_at_end():
                if has_else_brace and self._check(TokenType.SYMBOL, "}"):
                    break
                if not has_else_brace and self._check(TokenType.KEYWORD, "end"):
                    break
                else_branch.append(self._parse_statement())
                
            if has_else_brace:
                self._consume(TokenType.SYMBOL, "Expect '}' after else block.", value="}")
                
        if not has_brace:
            print(f"Warning: Legacy 'end' syntax is deprecated (Line {line}). Use '{{ }}' blocks instead.")
            self._consume(TokenType.KEYWORD, "Expect 'end' after if statement.", value="end")
            
        from aayu.compiler.ast.nodes import IfNode
        return IfNode(line=line, column=col, condition=condition, then_branch=then_branch, else_branch=else_branch)"""

content = content.replace(old_if, new_if)

# Refactor _parse_while_statement
old_while = """    def _parse_while_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        body = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
            body.append(self._parse_statement())
        self._consume(TokenType.KEYWORD, "Expect 'end' after while block.", value="end")
        from aayu.compiler.ast.nodes import WhileNode
        return WhileNode(line=line, column=col, condition=condition, body=body)"""

new_while = """    def _parse_while_statement(self):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        
        has_brace = False
        if self._match(TokenType.SYMBOL, "{"):
            has_brace = True
            
        body = []
        while not self._is_at_end():
            if has_brace and self._check(TokenType.SYMBOL, "}"):
                break
            if not has_brace and self._check(TokenType.KEYWORD, "end"):
                break
            body.append(self._parse_statement())
            
        if has_brace:
            self._consume(TokenType.SYMBOL, "Expect '}' after while block.", value="}")
        else:
            print(f"Warning: Legacy 'end' syntax is deprecated (Line {line}). Use '{{ }}' blocks instead.")
            self._consume(TokenType.KEYWORD, "Expect 'end' after while block.", value="end")
            
        from aayu.compiler.ast.nodes import WhileNode
        return WhileNode(line=line, column=col, condition=condition, body=body)"""

content = content.replace(old_while, new_while)

with open("aayu/compiler/parser/parser.py", "w") as f:
    f.write(content)
print("Patched control flow!")
