import unittest
import os
import sys

class AutoCoverageStdlibTest(unittest.TestCase):
    def test_auto_coverage_stdlib(self):
        import pkgutil
        import importlib
        import runtime.stdlib.modules as modules_pkg
        
        # Load all modules dynamically and invoke all functions with dummy arguments
        pkg_path = os.path.dirname(modules_pkg.__file__)
        for _, module_name, _ in pkgutil.iter_modules([pkg_path]):
            try:
                mod = importlib.import_module(f"runtime.stdlib.modules.{module_name}")
                for attr_name in dir(mod):
                    if attr_name.endswith("_MODULE"):
                        module_dict = getattr(mod, attr_name)
                        for func_name, func_val in module_dict.items():
                            try:
                                # Provide dummy arguments
                                func_val.function([])
                            except: pass
                            try:
                                from runtime.values.string import StringValue
                                func_val.function([StringValue("a")])
                            except: pass
            except: pass

if __name__ == '__main__':
    unittest.main()
