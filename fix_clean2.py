import sys

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = "        elif isinstance(hir, HIRLetDecl):\n            print(f'HIRLetDecl! {hir.name}')"
    new_target = "        elif isinstance(hir, HIRLetDecl):"

    content = content.replace(target, new_target)

    with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Cleaned up pipeline prints!")

patch()
