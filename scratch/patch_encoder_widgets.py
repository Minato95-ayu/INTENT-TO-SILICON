
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/bytecode/encoder.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

import re
new_widgets = """
WIDGET_TYPES = {
    "PAGE": 1,
    "COLUMN": 2,
    "ROW": 3,
    "CONTAINER": 4,
    "CARD": 5,
    "TEXT": 6,
    "HEADING": 7,
    "BUTTON": 8,
    "INPUT": 9,
    "IMAGE": 10,
    "STACK": 11,
    "PADDING": 12,
    "MARGIN": 13,
    "ALIGN": 14,
    "EXPANDED": 15,
    "SPACER": 16,
    "ICON": 17,
    "COMPONENT": 18,
    "LIST": 19,
    "GRID": 20,
    "CENTER": 21,
    "DIVIDER": 22,
    "SCROLLVIEW": 23,
    "APPBAR": 24,
    "NAVIGATIONBAR": 25,
    "DRAWER": 26,
    "DIALOG": 27,
    "SNACKBAR": 28,
    "PROGRESS": 29,
    "AVATAR": 30,
    "CHECKBOX": 31,
    "RADIO": 32,
    "SWITCH": 33,
    "DROPDOWN": 34,
    "TABBAR": 35,
    "FORM": 36,
    "PASSWORDINPUT": 37
}
"""
c = re.sub(r"WIDGET_TYPES = \{[\s\S]*?\}", new_widgets.strip(), c)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

