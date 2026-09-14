import re

with open("compiler/parser/parser.py", "r", encoding="utf-8") as f:
    content = f.read()

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
        from compiler.ast.nodes import IfNode
        return IfNode(line=line, column=col, condition=condition, then_branch=then_branch, else_branch=else_branch)"""

new_if = """    def _parse_if_statement(self, is_elif=False):
        line, col = self._previous().line, self._previous().column
        condition = self._parse_expression()
        then_branch = []
        while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end") and not self._check(TokenType.KEYWORD, "else") and not self._check(TokenType.KEYWORD, "elif"):
            then_branch.append(self._parse_statement())
            
        else_branch = None
        if self._match(TokenType.KEYWORD, "elif"):
            else_branch = [self._parse_if_statement(is_elif=True)]
        elif self._match(TokenType.KEYWORD, "else"):
            else_branch = []
            while not self._is_at_end() and not self._check(TokenType.KEYWORD, "end"):
                else_branch.append(self._parse_statement())
                
        if not is_elif:
            self._consume(TokenType.KEYWORD, "Expect 'end' after if statement.", value="end")
            
        from compiler.ast.nodes import IfNode
        return IfNode(line=line, column=col, condition=condition, then_branch=then_branch, else_branch=else_branch)"""

content = content.replace(old_if, new_if)

with open("compiler/parser/parser.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched if statement logic for elif")
