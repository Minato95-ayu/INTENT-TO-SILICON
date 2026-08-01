
import os

encoder_path = "compiler/bytecode/encoder.py"
with open(encoder_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "if rel.type == `"CALL`":", 
    "if rel.type in (`"CALL`", `"ACTION`"):"
)

with open(encoder_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched!")

