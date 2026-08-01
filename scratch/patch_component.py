
import os

# 1. Update encoder.py
encoder_path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/bytecode/encoder.py"
with open(encoder_path, "r", encoding="utf-8") as f:
    c = f.read()
if "\"ICON\": 17" in c and "\"COMPONENT\": 18" not in c:
    c = c.replace("\"ICON\": 17,", "\"ICON\": 17,\n    \"COMPONENT\": 18,")
    with open(encoder_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched encoder.py")

# 2. Update registry.py
registry_path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/runtime/ui/registry.py"
with open(registry_path, "r", encoding="utf-8") as f:
    c = f.read()
if "17: \"Icon\"" in c and "18: \"Component\"" not in c:
    c = c.replace("17: \"Icon\"", "17: \"Icon\",\n        18: \"Component\"")
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched registry.py")

# 3. Update interpreter.py
interpreter_path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/runtime/vm/interpreter.py"
with open(interpreter_path, "r", encoding="utf-8") as f:
    c = f.read()
old_list = "if type_name in [\"Page\", \"Column\", \"Row\", \"Container\", \"Card\"]:"
new_list = "if type_name in [\"Page\", \"Column\", \"Row\", \"Container\", \"Card\", \"Component\"]:"
if old_list in c:
    c = c.replace(old_list, new_list)
    with open(interpreter_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched interpreter.py")

# 4. Update .aayu files
for file in ["stthomas_app/components/navbar.aayu", "stthomas_app/components/home.aayu", "stthomas_app/components/notices.aayu"]:
    p = os.path.join("D:/intent-to-silicon-research/INTENT-TO-SILICON", file)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        if "page Navbar" in c:
            c = c.replace("page Navbar", "component Navbar")
        if "page Home" in c:
            c = c.replace("page Home", "component Home")
        if "page NoticesList" in c:
            c = c.replace("page NoticesList", "component NoticesList")
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Patched {file}")

