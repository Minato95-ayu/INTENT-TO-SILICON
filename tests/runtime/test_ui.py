import unittest
from typing import Any, Dict
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.ui.runtime import UIRuntime
from runtime.plugins.ui.widgets import UIElement, Page, Button, Text, Layout

class TestUIRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.ui = UIRuntime()
        self.kernel.registry.register(self.ui)
        self.kernel.boot()

    def tearDown(self):
        self.kernel.shutdown()

    def test_tree_generation(self):
        ast = {
            "type": "Page",
            "props": {"title": "Home"},
            "children": [
                {
                    "type": "Layout",
                    "props": {"type": "Column"},
                    "children": [
                        {"type": "Text", "props": {"text": "Counter: 0"}},
                        {"type": "Button", "props": {"label": "Add"}}
                    ]
                }
            ]
        }
        
        res = self.kernel.dispatch("ui", "build", {"ast": ast})
        self.assertTrue(res.success)
        
        root = res.data["tree"]
        self.assertIsInstance(root, Page)
        self.assertEqual(root.props["title"], "Home")
        
        # Verify IDs are generated
        self.assertIsNotNone(root.id)
        self.assertTrue(isinstance(root.id, str))
        
        # Verify children
        self.assertEqual(len(root.children), 1)
        col = root.children[0]
        self.assertIsInstance(col, Layout)
        self.assertEqual(col.props["type"], "Column")
        self.assertIsNotNone(col.id)
        
        self.assertEqual(len(col.children), 2)
        text_node = col.children[0]
        btn_node = col.children[1]
        
        self.assertIsInstance(text_node, Text)
        self.assertEqual(text_node.props["text"], "Counter: 0")
        
        self.assertIsInstance(btn_node, Button)
        self.assertEqual(btn_node.props["label"], "Add")

    def test_reactive_mini_tree(self):
        # A subset AST that represents just a single widget update
        mini_ast = {
            "id": "text-widget-123",  # Existing ID to maintain identity
            "type": "Text",
            "props": {"text": "Counter: 1"},
            "children": []
        }
        
        res = self.kernel.dispatch("ui", "build_mini_tree", {"ast": mini_ast})
        self.assertTrue(res.success)
        
        node = res.data["tree"]
        self.assertIsInstance(node, Text)
        self.assertEqual(node.id, "text-widget-123")
        self.assertEqual(node.props["text"], "Counter: 1")

    def test_invalid_widget_type(self):
        ast = {
            "type": "UnknownWidget",
            "props": {},
            "children": []
        }
        res = self.kernel.dispatch("ui", "build", {"ast": ast})
        self.assertFalse(res.success)
        self.assertIn("Unknown widget type", res.error)

if __name__ == '__main__':
    unittest.main()
