
import os

with open("compiler/bytecode/encoder.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace(
    "widget_type_id = WIDGET_TYPES.get(widget_type_str, 0)",
    """widget_type_id = WIDGET_TYPES.get(widget_type_str, 0)
        print(f"[ENCODER WIDGET TYPE] {widget_type_str} -> id={widget_type_id}, WIDGET_TYPES={list(WIDGET_TYPES.keys())}")"""
)
with open("compiler/bytecode/encoder.py", "w", encoding="utf-8") as f:
    f.write(code)

