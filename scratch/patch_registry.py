
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/runtime/ui/registry.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

new_registry = """
class WidgetRegistry:
    _widgets: Dict[int, str] = {
        1: "Page",
        2: "Column",
        3: "Row",
        4: "Container",
        5: "Card",
        6: "Text",
        7: "Heading",
        8: "Button",
        9: "Input",
        10: "Image",
        11: "Stack",
        12: "Padding",
        13: "Margin",
        14: "Align",
        15: "Expanded",
        16: "Spacer",
        17: "Icon",
        18: "Component",
        19: "List",
        20: "Grid",
        21: "Center",
        22: "Divider",
        23: "ScrollView",
        24: "AppBar",
        25: "NavigationBar",
        26: "Drawer",
        27: "Dialog",
        28: "Snackbar",
        29: "Progress",
        30: "Avatar",
        31: "Checkbox",
        32: "Radio",
        33: "Switch",
        34: "Dropdown",
        35: "TabBar",
        36: "Form",
        37: "PasswordInput"
    }
"""
import re
c = re.sub(r"class WidgetRegistry:[\s\S]*?    \}", new_registry.strip(), c)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

