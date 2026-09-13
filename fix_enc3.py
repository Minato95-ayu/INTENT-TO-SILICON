
import os
with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\"SCAFFOLD\": 39", "\"SCAFFOLD\": 39,\n    \"CHART\": 100,\n    \"DATAFRAMEWIDGET\": 101")
with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Widgets added.")

