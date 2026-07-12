import os
import re

def update_file(filepath, header, func_comments=None):
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
            if comment.strip()[:10] not in content:
                replacement = r"\1\n" + comment
                content = re.sub(pattern, replacement, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Commented: {filepath}")

base = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype'

# --- 6. BYTECODE / INSTRUCTIONS ---
bc_header = '''"""
===============================================================================
AAYU Compiler - Bytecode ISA (Instruction Set Architecture)

Purpose:
    Yahan AAYU Virtual Machine ke saare Opcodes (Instructions) define hote hain.

Input:
    None

Output:
    Constants (e.g. OP_ADD = 1)

Pipeline:
    Compiler
        ↓
    Bytecode ISA ← (Current File)
        ↓
    Virtual Machine (VM)

Ye file kyun important hai?
    Ye dictionary/constants hai jise Compiler aur VM dono use karte hain agree karne ke liye ki 'OP_ADD' ka kya matlab hai.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    5. compiler.py
    6. runtime/vm/instructions.py (You are here)
    7. runtime/vm/vm.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/runtime/vm/instructions.py'), bc_header)

# --- 7. VIRTUAL MACHINE ---
vm_header = '''"""
===============================================================================
AAYU Compiler - Virtual Machine (VM)

Purpose:
    Ye AAYU ka Engine hai. Ye compiler dwara diye gaye Bytecode ko read karke execute karta hai.

Input:
    Bytecode Instructions, Constants

Output:
    Program Execution (Prints, State changes, etc)

Pipeline:
    Bytecode ISA
        ↓
    Virtual Machine (VM) ← (Current File)
        ↓
    Memory / CPU Execution

Ye file kyun important hai?
    Jab aap 'aayu run' karte hain, to yahi file chal rahi hoti hai. Isme ek Infinite 'while' loop hota hai jo ek-ek instruction fetch karta hai aur run karta hai.

Difficulty:
    ⭐⭐⭐⭐ (Very Hard)

Recommended Reading Order:
    6. runtime/vm/instructions.py
    7. runtime/vm/vm.py (You are here)
    8. runtime/stdlib/stdlib.py
===============================================================================
"""'''
vm_funcs = {
    "run": '''        """
        Purpose:
            VM ka main execution loop.

        Steps:
            1. Instruction Pointer (ip) check karo.
            2. Current instruction read karo (fetch).
            3. Opcode ke hisaab se execute karo (dispatch).
            4. Jab tak HALT na aaye, chalte raho.
        """'''
}
update_file(os.path.join(base, 'language/runtime/vm/vm.py'), vm_header, vm_funcs)

# --- 8. RUNTIME STDLIB ---
rt_header = '''"""
===============================================================================
AAYU Compiler - Runtime Standard Library

Purpose:
    Isme native functions hote hain (jaise print(), len(), etc) jo AAYU scripts direct call kar sakti hain.

Pipeline:
    Virtual Machine (VM)
        ↓
    Standard Library ← (Current File)

Ye file kyun important hai?
    AAYU apne aap me I/O (input/output) nahi kar sakti. Use Python/OS ki madad leni padti hai (jaise console par print karna). Ye file un native capabilities ka bridge hai.

Difficulty:
    ⭐⭐ (Medium)

Recommended Reading Order:
    7. runtime/vm/vm.py
    8. runtime/stdlib/stdlib.py (You are here)
    9. runtime/memory/manager.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/runtime/stdlib/stdlib.py'), rt_header)

# --- 9. MEMORY MANAGER ---
mem_header = '''"""
===============================================================================
AAYU Compiler - Memory Manager (DARC)

Purpose:
    Variables aur Objects kahan save honge aur kab delete honge, ye file manage karti hai. (Deterministic ARC)

Pipeline:
    Virtual Machine (VM)
        ↓
    Memory Manager ← (Current File)

Ye file kyun important hai?
    Agar memory delete nahi hui to Memory Leak ho jayega (RAM full). Ye ref-counting use karta hai object clean karne ke liye.

Difficulty:
    ⭐⭐⭐ (Hard)

Recommended Reading Order:
    8. runtime/stdlib/stdlib.py
    9. runtime/memory/manager.py (You are here)
    10. workspace/workspace.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/runtime/memory/manager.py'), mem_header)

# --- 10. PACKAGE MANAGER ---
pkg_header = '''"""
===============================================================================
AAYU Compiler - Package & Workspace Manager

Purpose:
    Projects, Modules aur 'aayu.mod' files ko load aur resolve karta hai.

Pipeline:
    Memory Manager
        ↓
    Package Manager ← (Current File)

Ye file kyun important hai?
    Bade projects multiple files me hote hain. Ye file ensure karti hai ki 'import utils' likhne par sahi file load ho.

Difficulty:
    ⭐⭐ (Medium)

Recommended Reading Order:
    9. runtime/memory/manager.py
    10. workspace/workspace.py (You are here)
    11. brainos/orchestrator.py
===============================================================================
"""'''
update_file(os.path.join(base, 'language/workspace/workspace.py'), pkg_header)

# --- 11. BRAINOS ORCHESTRATOR ---
brain_header = '''"""
===============================================================================
AAYU Compiler - BrainOS Orchestrator

Purpose:
    Ye AI-driven subsystem hai jo Intent Engine se milne wale Graph ko AAYU code me architect karta hai.

Pipeline:
    Package Manager
        ↓
    BrainOS Orchestrator ← (Current File)

Ye file kyun important hai?
    AAYU language ki sabse badi khasiyat yahi hai. Ye 'Build Instagram' jaise text ko samajh kar file structure aur AST scaffold generate karta hai.

Difficulty:
    ⭐⭐⭐⭐ (Very Hard)

Recommended Reading Order:
    10. workspace/workspace.py
    11. brainos/orchestrator.py (You are here)
    End of Core Path!
===============================================================================
"""'''
update_file(os.path.join(base, 'brainos/orchestrator.py'), brain_header)

print("Done updating batch 3")
