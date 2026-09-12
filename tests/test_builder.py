import pytest
import os
from tools.builder.builder import Builder

def test_builder_windows():
    builder = Builder(mode="release")
    builder.build("windows")
    
    exe_path = os.path.join("build", "release", "app.exe")
    assert os.path.exists(exe_path)
    
    with open(exe_path, "rb") as f:
        content = f.read()
    assert content.startswith(b"MZ")
    
def test_builder_web():
    builder = Builder(mode="release")
    builder.build("web")
    
    html_path = os.path.join("build", "web", "index.html")
    assert os.path.exists(html_path)
    
    with open(html_path, "r") as f:
        content = f.read()
    assert '<div id="app">' in content
    assert "<title>AAYU Web App</title>" in content

if __name__ == '__main__':
    pytest.main(['-v', __file__])



