import os
import re

def update_file(filepath, header, func_comments=None, inline_comments=None):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('"""'):
        end_idx = content.find('"""', 3)
        if end_idx != -1:
            content = header + "\n" + content[end_idx+3:].lstrip()
    else:
        content = header + "\n\n" + content
        
    if func_comments:
        for func_name, comment in func_comments.items():
            pattern = r"(def\s+" + func_name + r"\s*\([^)]*\)(?:\s*->\s*[^:]+)?:)"
            # Only replace if not already commented
            if comment.strip()[:10] not in content:
                replacement = r"\1\n" + comment
                content = re.sub(pattern, replacement, content, count=1)

    if inline_comments:
        for target, inline_comment in inline_comments.items():
            if inline_comment not in content:
                content = content.replace(target, inline_comment + "\n" + target)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Commented: {filepath}")

base = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype'

# --- 2. PARSER ---
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
    Lexer
        ↓
    Parser   ← (Current File)
        ↓
    AST
        ↓
    Semantic Analysis

Ye file kyun important hai?
    Agar parser galat hoga, to compiler code ke structure ko galat samjhega aur aage ka process fail ho jayega. Ye ek hand-written recursive descent parser hai.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    1. lexer.py
    2. parser.py (You are here)
    3. ast_nodes.py
===============================================================================
"""'''
parser_funcs = {
    "parse_program": '''        """
        Purpose:
            Poore file/program ko parse karta hai jab tak EOF na mil jaye.

        Example Input:
            entity User end.

        Output:
            ProgramNode(body=[EntityNode(...)])

        Steps:
            1. Jab tak file ka end (EOF) nahi aata.
            2. parse_statement() call karte raho.
            3. Sabhi statements ko ProgramNode me daal kar return karo.
        """''',
    "parse_statement": '''        """
        Purpose:
            Single statement parse karta hai (Jaise Variable declare karna, Print karna).
        """''',
    "advance": '''        """
        Purpose:
            Current token ko consume karke agle token par jump karta hai.
        """'''
}
parser_inline = {
    'def advance(self):': '    # Token stream me aage badhne ke liye.',
    'if self.match("KEYWORD", "entity"):': '        # Agar entity keyword mila, to Entity parse karo.'
}
update_file(os.path.join(base, 'language/parser.py'), parser_header, parser_funcs, parser_inline)


# --- 3. AST NODES ---
ast_header = '''"""
===============================================================================
AAYU Compiler - Abstract Syntax Tree (AST) Nodes

Purpose:
    Ye file mein wo classes hain jo code ke structure ko Memory me save karti hain (Nodes).

Input:
    None (Ye sirf Data Structures hain)

Output:
    AST Objects used by Parser

Pipeline:
    Parser
        ↓
    AST      ← (Current File)
        ↓
    Semantic Analysis
        ↓
    Compiler

Ye file kyun important hai?
    Poore Compiler aur BrainOS ko yahi nodes padh kar samajh aata hai ki code me kya likha hai. Jaise ek VariableNode ka naam aur value kya hai.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    2. parser.py
    3. ast_nodes.py (You are here)
    4. passes/semantic/type_checker.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/ast_nodes.py'), ast_header)


# --- 4. SEMANTIC ANALYZER ---
sem_header = '''"""
===============================================================================
AAYU Compiler - Semantic Analyzer (Type Checker)

Purpose:
    Ye file AST ko check karti hai ki kya code statically safe hai. 
    (Kahin string me number to add nahi ho raha?)

Input:
    Abstract Syntax Tree (AST)

Output:
    Validated AST (ya Compile-time Error)

Pipeline:
    AST
        ↓
    Semantic Analysis ← (Current File)
        ↓
    Compiler

Ye file kyun important hai?
    AAYU ek strict typed language hai. Agar types galat hue to ye runtime par crash hone se bachata hai.

Difficulty:
    ⭐⭐ (Medium)

Recommended Reading Order:
    3. ast_nodes.py
    4. passes/semantic/type_checker.py (You are here)
    5. compiler.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/passes/semantic/type_checker.py'), sem_header)


# --- 5. COMPILER ---
compiler_header = '''"""
===============================================================================
AAYU Compiler - Bytecode Compiler

Purpose:
    Ye file Validated AST ko AAYU Bytecode (Low-level instructions) me convert karti hai.

Input:
    Validated AST

Output:
    List of Bytecode Instructions

Pipeline:
    Semantic Analysis
        ↓
    Compiler ← (Current File)
        ↓
    Bytecode ISA
        ↓
    Virtual Machine (VM)

Ye file kyun important hai?
    VM seedhe AST run nahi kar sakta. Use bytes me low-level instructions chahiye hote hain (Jaise LOAD, ADD, JUMP). Ye file wahi bytecode generate karti hai.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    4. passes/semantic/type_checker.py
    5. compiler.py (You are here)
    6. bytecode.py
===============================================================================
"""'''
compiler_funcs = {
    "compile": '''        """
        Purpose:
            AST Node types par dispatch karke compile karta hai.
        """''',
    "visit_binary_op": '''        """
        Purpose:
            Math operations (jaise +, -) ko compile karta hai.

        Steps:
            1. Left side ko compile karo (push on stack)
            2. Right side ko compile karo (push on stack)
            3. Operator ka Opcode emit karo (jo pop karega dono ko)
        """'''
}
update_file(os.path.join(base, 'language/compiler.py'), compiler_header, compiler_funcs)


# --- 6. BYTECODE ---
bc_header = '''"""
===============================================================================
AAYU Compiler - Bytecode ISA (Instruction Set Architecture)

Purpose:
    Yahan AAYU Virtual Machine ke saare Opcodes (Instructions) define hote hain.

Input:
    None

Output:
    Constants & Formats

Pipeline:
    Compiler
        ↓
    Bytecode ISA ← (Current File)
        ↓
    Virtual Machine (VM)

Ye file kyun important hai?
    Ye dictionary hai jise Compiler aur VM dono use karte hain agree karne ke liye ki 'OP_ADD' ka kya matlab hai.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    5. compiler.py
    6. bytecode.py (You are here)
    7. runtime/vm/vm.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/bytecode.py'), bc_header)

print("Done updating batch 2")
