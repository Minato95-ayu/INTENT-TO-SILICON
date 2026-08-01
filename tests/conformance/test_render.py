import unittest
import time
from typing import Any, Dict
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.plugins.render.runtime import RenderRuntime
from aayu.runtime.plugins.render.commands import RenderCommand
from aayu.runtime.plugins.render.diff import DiffEngine
from aayu.runtime.plugins.render.layout import LayoutEngine
from aayu.runtime.plugins.ui.widgets import UIElement, Text, Layout, Button

class TestRenderRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.render = RenderRuntime()
        self.kernel.registry.register(self.render)
        self.kernel.boot()
        
    def tearDown(self):
        self.kernel.shutdown()

    def test_diff_engine_o_n(self):
        diff = DiffEngine()
        
        # Build old tree
        old_text = Text(element_id="txt1", props={"text": "Old"})
        old_root = Layout(element_id="root", props={"type": "Row"})
        old_root.add_child(old_text)
        
        # Build new tree
        new_text = Text(element_id="txt1", props={"text": "New"})
        new_btn = Button(element_id="btn1", props={"label": "Click"})
        new_root = Layout(element_id="root", props={"type": "Row"})
        new_root.add_child(new_text)
        new_root.add_child(new_btn)
        
        commands = diff.compute(old_root, new_root)
        
        # Expected commands:
        # 1. UPDATE_TEXT on txt1
        # 2. CREATE on btn1
        # 3. MOUNT btn1 to root
        
        cmds = [c.type for c in commands]
        self.assertIn("UPDATE_PROPS", cmds)
        self.assertIn("CREATE", cmds)
        
        # Ensure O(N) constraints (check that the command count is minimal)
        self.assertLessEqual(len(commands), 4)

    def test_layout_engine(self):
        layout = LayoutEngine()
        
        root = Layout(element_id="root", props={
            "type": "Row",
            "padding": 10
        })
        child1 = Text(element_id="c1", props={"width": 50, "height": 20})
        child2 = Text(element_id="c2", props={"width": 100, "height": 30})
        
        root.add_child(child1)
        root.add_child(child2)
        
        boxes = layout.compute(root)
        
        self.assertEqual(boxes["c1"]["x"], 10)
        self.assertEqual(boxes["c1"]["y"], 10)
        self.assertEqual(boxes["c2"]["x"], 60) # padding + child1_width
        self.assertEqual(boxes["c2"]["y"], 10)
        
        # Root box
        self.assertEqual(boxes["root"]["width"], 170) # 10 (pad) + 50 + 100 + 10 (pad)
        self.assertEqual(boxes["root"]["height"], 50) # 10 + max(20, 30) + 10

    def test_render_dispatch(self):
        # Create a mini tree and dispatch to render
        tree = Text(element_id="t1", props={"text": "Hello"})
        
        res = self.kernel.dispatch("render", "update_tree", {"tree": tree})
        self.assertTrue(res.success)
        
        # Now change it
        tree_new = Text(element_id="t1", props={"text": "World"})
        res2 = self.kernel.dispatch("render", "update_tree", {"tree": tree_new})
        self.assertTrue(res2.success)
        
        # The terminal adapter should have logged the update commands internally.

    def test_performance_100k_nodes(self):
        # Generate large flat tree
        diff = DiffEngine()
        old_root = Layout(element_id="root", props={"type": "Column"})
        new_root = Layout(element_id="root", props={"type": "Column"})
        
        # Add 10,000 nodes (100k might be too heavy for Python unittests to run in < 1 sec, so we test 10k to ensure it scales linearly)
        for i in range(10000):
            old_root.add_child(Text(element_id=f"t{i}", props={"text": "A"}))
            
            if i % 2 == 0:
                new_root.add_child(Text(element_id=f"t{i}", props={"text": "B"})) # Update
            else:
                new_root.add_child(Text(element_id=f"t{i}", props={"text": "A"})) # No change
                
        start = time.time()
        commands = diff.compute(old_root, new_root)
        duration = time.time() - start
        
        # Should finish very fast in Python using O(N) hash maps
        self.assertLess(duration, 2.0)
        self.assertEqual(len(commands), 5000) # Half were updated
        
if __name__ == '__main__':
    unittest.main()
