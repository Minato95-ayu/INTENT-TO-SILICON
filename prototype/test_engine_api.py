import os
import sys

# Ensure prototype is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
prototype_dir = current_dir
sys.path.insert(0, prototype_dir)

from engine.api import AAYUEngine

def test_engine_validate():
    source = "number age is 20. show age."
    engine = AAYUEngine()
    project = engine.load_source(source)
    
    ast = project.validate()
    assert ast is not None
    assert len(ast.statements) == 2
    
def test_engine_run():
    source = "number score is 100."
    engine = AAYUEngine()
    project = engine.load_source(source)
    project.run()
    # If no exception, it ran successfully.
    assert True

if __name__ == "__main__":
    test_engine_validate()
    test_engine_run()
    print("Engine API tests passed.")
