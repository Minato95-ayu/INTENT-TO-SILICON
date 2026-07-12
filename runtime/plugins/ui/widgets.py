import uuid
from typing import Any, Dict, List, Optional

class UIElement:
    """Base class for all logical UI widgets."""
    def __init__(self, element_id: Optional[str] = None, props: Optional[Dict[str, Any]] = None):
        self.id = element_id or str(uuid.uuid4())
        self.props = props or {}
        self.children: List['UIElement'] = []
        self.parent: Optional['UIElement'] = None

    def add_child(self, child: 'UIElement'):
        child.parent = self
        self.children.append(child)

    def to_dict(self) -> Dict[str, Any]:
        """Convert logical node to dict for diffing purposes."""
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "props": self.props,
            "children": [c.to_dict() for c in self.children]
        }


class Page(UIElement): pass
class Layout(UIElement): pass
class Container(UIElement): pass
class Button(UIElement): pass
class Text(UIElement): pass
class Image(UIElement): pass
class Input(UIElement): pass
class List(UIElement): pass
class Card(UIElement): pass

# Widget registry mapping
WIDGET_REGISTRY = {
    "Page": Page,
    "Layout": Layout,
    "Container": Container,
    "Button": Button,
    "Text": Text,
    "Image": Image,
    "Input": Input,
    "List": List,
    "Card": Card
}
