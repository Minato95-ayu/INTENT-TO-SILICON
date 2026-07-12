import unittest
import time
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.ui.runtime import UIRuntime
from runtime.plugins.render.runtime import RenderRuntime

class TestWidgetStress(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.ui_runtime = UIRuntime()
        self.render_runtime = RenderRuntime()
        self.kernel.registry.register(self.ui_runtime)
        self.kernel.registry.register(self.render_runtime)

    def test_100k_widgets(self):
        """Stress test rendering 100,000 widgets."""
        start_time = time.time()
        
        # Build a massive UI tree
        self.kernel.dispatch("ui", "build", {"type": "Page", "name": "StressPage"})
        for i in range(100_000):
            # We mock the build dispatch
            self.kernel.dispatch("ui", "build", {"type": "Text", "name": f"TextWidget{i}", "props": {"text": str(i)}})
            
        build_time = time.time() - start_time
        
        # Mock rendering the tree
        start_render = time.time()
        self.kernel.dispatch("render", "draw", {"target": "StressPage"})
        render_time = time.time() - start_render
        
        # Assertions
        # In a real stress test, we might just assert it completes within a time limit
        # e.g., less than 5 seconds
        self.assertTrue(build_time < 5.0, f"Building 100k widgets took too long: {build_time}s")
        self.assertTrue(render_time < 5.0, f"Rendering 100k widgets took too long: {render_time}s")

if __name__ == '__main__':
    unittest.main()
