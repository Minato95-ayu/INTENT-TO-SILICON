import pytest
from aayu.runtime.ui.render_tree import RenderNode, RenderTree
from aayu.runtime.layout.engine import LayoutEngine
from aayu.runtime.ui.painter import Painter
from aayu.runtime.ui.display_list import DrawRect, DrawText

def test_render_node_id_generation():
    node = RenderNode("Button")
    assert node.id is not None
    assert len(node.id) > 10

def test_layout_engine_measure_and_layout():
    # Construct a simple RenderTree: Page -> Container -> Button
    page = RenderNode("Page")
    container = RenderNode("Container")
    button = RenderNode("Button", props={"value": "Click Me"})
    
    container.add_child(button)
    page.add_child(container)
    
    layout_engine = LayoutEngine(800, 600)
    layout_root = layout_engine.calculate_layout(page)
    
    # Assert layout root dimensions
    assert layout_root.render_node.type == "Page"
    assert layout_root.width == 800
    assert layout_root.height > 0
    
    # Assert container dimensions
    layout_container = layout_root.children[0]
    assert layout_container.render_node.type == "Container"
    assert layout_container.width > 0
    assert layout_container.height > 0
    assert layout_container.x == 5 # Based on our naive _layout implementation, Page padding is 5 on y, 5 on x.
    assert layout_container.y == 5

    # Assert button dimensions
    layout_button = layout_container.children[0]
    assert layout_button.render_node.type == "Button"
    assert layout_button.width > 0
    assert layout_button.height == 30 # Button height is hardcoded to 30 in our mock
    assert layout_button.x == 15 # Container adds x+10, so 5 + 10 = 15
    assert layout_button.y == 15 # Container y=5 + 10 padding = 15

def test_display_list_builder():
    page = RenderNode("Page")
    button = RenderNode("Button", props={"value": "Submit"})
    page.add_child(button)
    
    layout_engine = LayoutEngine(800, 600)
    layout_root = layout_engine.calculate_layout(page)
    
    painter = Painter()
    dl = painter.paint(layout_root)
    
    # Assert commands are generated
    assert len(dl.commands) > 0
    
    # We should have a DrawRect (or RoundedRect) for the page, and DrawText for the button
    has_text = any(isinstance(cmd, DrawText) and cmd.text == "Submit" for cmd in dl.commands)
    assert has_text, "DrawText command for the button should be present"
