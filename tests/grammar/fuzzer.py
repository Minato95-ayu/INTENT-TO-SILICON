import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.lexer.lexer import Lexer, TokenType, Token
from aayu.compiler.parser.parser import Parser
from aayu.compiler.errors import DiagnosticEngine

def run_fuzzer(iterations=10000):
    print(f"Starting Grammar Fuzzing: {iterations} random token streams...")
    types = list(TokenType)
    crashes = 0
    
    for i in range(iterations):
        # Generate random length token stream
        length = random.randint(1, 50)
        tokens = []
        for _ in range(length):
            t_type = random.choice(types)
            val = "rand" if t_type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.KEYWORD) else str(random.randint(0, 99))
            tokens.append(Token(t_type, val, 1, 1, "source"))
            
        tokens.append(Token(TokenType.EOF, "", 1, 1, ""))
        
        diag = DiagnosticEngine()
        parser = Parser(tokens, diag=diag)
        try:
            parser.parse()
        except Exception as e:
            crashes += 1
            
    print(f"Fuzzing Complete. Crashes: {crashes}")
    with open(os.path.join(os.path.dirname(__file__), "fuzzer_report.txt"), "w") as f:
        f.write(str(crashes))
    return crashes == 0

if __name__ == "__main__":
    success = run_fuzzer()
    sys.exit(0 if success else 1)
