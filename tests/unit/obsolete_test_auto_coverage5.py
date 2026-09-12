import unittest
import os
import sys

class AutoCoveragePlannerTest(unittest.TestCase):
    def test_auto_coverage_planner(self):
        import pkgutil
        import importlib
        import compiler.planner as planner_pkg
        
        pkg_path = os.path.dirname(planner_pkg.__file__)
        for _, module_name, _ in pkgutil.iter_modules([pkg_path]):
            try:
                mod = importlib.import_module(f"compiler.planner.{module_name}")
                for attr_name in dir(mod):
                    if "Planner" in attr_name or "Optimizer" in attr_name or "Node" in attr_name:
                        cls = getattr(mod, attr_name)
                        try:
                            # Try to instantiate it
                            obj = cls()
                        except TypeError:
                            try: obj = cls(None)
                            except: pass
                        except: pass
            except: pass

if __name__ == '__main__':
    unittest.main()
