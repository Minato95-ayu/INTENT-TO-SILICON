import sys
import os
import unittest

def handle(args):
    print("[AAYU] Running test suite...")
    
    test_dir = "tests"
    if len(args) > 0 and not args[0].startswith("-"):
        test_dir = args[0]
        
    if not os.path.exists(test_dir):
        print(f"Error: Test directory '{test_dir}' not found.")
        sys.exit(1)
        
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)
