import sys

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Add a print statement to _hir_to_mir
    if "print(f'HIRLetDecl! {hir.name}')" not in content:
        content = content.replace(
            "        elif isinstance(hir, HIRLetDecl):",
            "        elif isinstance(hir, HIRLetDecl):\n            print(f'HIRLetDecl! {hir.name}')"
        )
    with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
        f.write(content)

patch()
