import os
import re

def update_file(filepath, header, func_comments, inline_comments):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace or prepend the header
    if content.startswith('"""'):
        end_idx = content.find('"""', 3)
        if end_idx != -1:
            content = header + "\n" + content[end_idx+3:].lstrip()
    else:
        content = header + "\n\n" + content
        
    # 2. Inject function comments
    for func_name, comment in func_comments.items():
        # Match 'def func_name(args):' and insert comment inside it
        # Try to avoid re-commenting if it already exists
        if comment.strip()[:10] in content:
            continue
            
        pattern = r"(def\s+" + func_name + r"\s*\([^)]*\)(?:\s*->\s*[^:]+)?:)"
        replacement = r"\1\n" + comment
        content = re.sub(pattern, replacement, content, count=1)

    # 3. Inject inline comments
    for target, inline_comment in inline_comments.items():
        if inline_comment not in content:
            content = content.replace(target, inline_comment + "\n" + target)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully commented: {filepath}")

lexer_header = '''"""
===============================================================================
AAYU Compiler - Lexer

Purpose:
    Ye file raw source code (text) ko Tokens (words) me convert karti hai.

Input:
    Raw AAYU Source Code (string)

Output:
    List of Tokens

Pipeline:
    Source Code
        ↓
    Lexer    ← (Current File)
        ↓
    Parser
        ↓
    AST
        ↓
    Semantic Analysis

Ye file kyun important hai?
    Compiler seedhe text nahi padh sakta. Lexer pehla step hai jo text ko words (Keywords, Strings, Symbols) me classify karta hai taaki aage ka process aasan ho.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    1. lexer.py (You are here)
    2. parser.py
    3. ast_nodes.py
===============================================================================
"""'''

lexer_func = {
    "tokenize": '''        """
        Purpose:
            Regex patterns use karke source string ko tokens ki list me convert karta hai.

        Example Input:
            let a = 10.

        Output:
            [Token(KEYWORD, 'let'), Token(IDENTIFIER, 'a'), Token(EQ, '='), Token(NUMBER, '10'), Token(DOT, '.')]

        Steps:
            1. Har character pattern match karo.
            2. Whitespace aur Comments ignore karo.
            3. Matches ko Token list me save karo.
        """'''
}

lexer_inline = {
    'if kind in ("WHITESPACE", "COMMENT"):': '            # Comments aur spaces compiler ke kaam ke nahi hote, isliye skip karte hain.',
    'elif kind == "MISMATCH":': '            # Agar koi ajeeb character mile jo regex me na ho, to yahan syntax error aayega.'
}

# Apply to lexer
update_file(
    r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\lexer.py',
    lexer_header,
    lexer_func,
    lexer_inline
)

# ----------------- PARSER -----------------
parser_header = '''"""
===============================================================================
AAYU Compiler - Parser

Purpose:
    Ye file Lexer se aaye tokens ko padhti hai aur ek Abstract Syntax Tree (AST) banati hai.

Input:
    Token stream (List of Tokens)

Output:
    Abstract Syntax Tree (AST)

Pipeline:
    Source Code
        ↓
    Lexer
        ↓
    Parser   ← (Current File)
        ↓
    AST
        ↓
    Semantic Analysis

Ye file kyun important hai?
    Agar parser galat hoga, to compiler code ke structure ko galat samjhega aur aage ka process fail ho jayega.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    1. lexer.py
    2. parser.py (You are here)
    3. ast_nodes.py
===============================================================================
"""'''

# We will apply parser updates in the next step to ensure accuracy
print("Done step 1.")
