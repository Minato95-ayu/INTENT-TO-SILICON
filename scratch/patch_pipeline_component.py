
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/ir/pipeline.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

old_code = """            if hir.w_type.lower() == "page":
                page_name = hir.props.get("name", "")"""

new_code = """            if hir.w_type.lower() in ["page", "component"]:
                page_name = hir.props.get("name", "")"""

if old_code in c:
    c = c.replace(old_code, new_code)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched pipeline.py")
else:
    print("Could not find old code in pipeline.py")

