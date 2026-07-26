from typing import Dict, Type

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
        37: "PasswordInput",
        38: "ChatBubble",
        39: "Scaffold"
    }

    @classmethod
    def get_widget_name(cls, widget_id: int) -> str:
        return cls._widgets.get(widget_id, f"UnknownWidget_{widget_id}")
        
    @classmethod
    def register_widget(cls, widget_id: int, name: str):
        cls._widgets[widget_id] = name
