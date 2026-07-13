import pytest
import os
import shutil
import tempfile
import zipfile
import json
from tools.package_manager.manager import PackageManager
from tools.package_manager.exceptions import CircularDependencyError, ManifestError, ChecksumMismatchError, PackageNotFoundError

@pytest.fixture
def mock_env():
    # Setup isolated test environment
    test_dir = tempfile.mkdtemp()
    
    # Setup mock home for ~/.aayu (Cache/Registry)
    home_dir = os.path.join(test_dir, "home")
    os.makedirs(home_dir)
    
    # Setup project directory
    project_dir = os.path.join(test_dir, "project")
    os.makedirs(project_dir)
    
    yield home_dir, project_dir
    
    # Teardown
    shutil.rmtree(test_dir)

def create_mock_package(home_dir, name, version, deps=None, checksum="dummy"):
    # This creates a package directly in the Mock Official Registry
    reg_dir = os.path.join(home_dir, ".aayu", "cache", "registry_mock", name)
    os.makedirs(reg_dir, exist_ok=True)
    
    # Create zip
    zip_path = os.path.join(reg_dir, f"{version}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("test.txt", f"Hello from {name} {version}")
        
    from tools.package_manager.security import SecurityInfo
    real_checksum = SecurityInfo.generate_checksum(zip_path)
    if checksum == "valid":
        checksum = real_checksum
        
    meta_path = os.path.join(reg_dir, "meta.json")
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            meta = json.load(f)
    else:
        meta = {"name": name, "owner": "test", "versions": {}}
        
    meta["versions"][version] = {
        "checksum": checksum,
        "dependencies": deps or {}
    }
    
    with open(meta_path, 'w') as f:
        json.dump(meta, f)
        
def test_pm_init(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    assert os.path.exists(os.path.join(project_dir, "aayu.json"))
    with open(os.path.join(project_dir, "aayu.json"), 'r') as f:
        data = json.load(f)
        assert data["name"] == "project"

def test_pm_install_and_cache(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    create_mock_package(home_dir, "ui", "1.0.0", checksum="valid")
    
    # Install specific package
    pm.install("ui")
    
    assert os.path.exists(os.path.join(project_dir, "aayu.json"))
    assert os.path.exists(os.path.join(project_dir, "aayu.lock"))
    assert os.path.exists(os.path.join(project_dir, ".aayu_modules", "ui", "test.txt"))
    
    # Check cache
    assert os.path.exists(os.path.join(home_dir, ".aayu", "packages", "ui@1.0.0.zip"))

def test_pm_remove(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    create_mock_package(home_dir, "ui", "1.0.0", checksum="valid")
    pm.install("ui")
    assert os.path.exists(os.path.join(project_dir, ".aayu_modules", "ui"))
    
    pm.remove("ui")
    assert not os.path.exists(os.path.join(project_dir, ".aayu_modules", "ui"))
    
    with open(os.path.join(project_dir, "aayu.json"), 'r') as f:
        data = json.load(f)
        assert "ui" not in data.get("dependencies", {})

def test_circular_dependency(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    create_mock_package(home_dir, "A", "1.0.0", deps={"B": "^1.0.0"}, checksum="valid")
    create_mock_package(home_dir, "B", "1.0.0", deps={"A": "^1.0.0"}, checksum="valid")
    
    with pytest.raises(CircularDependencyError):
        pm.install("A")

def test_checksum_mismatch(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    # Provide an invalid checksum intentionally
    create_mock_package(home_dir, "hacked_pkg", "1.0.0", checksum="invalid_hash_123")
    
    with pytest.raises(ChecksumMismatchError):
        pm.install("hacked_pkg")

def test_publish_and_search(mock_env):
    home_dir, project_dir = mock_env
    pm = PackageManager(root_dir=project_dir, mock_home=home_dir)
    pm.init()
    
    # Login
    pm.login("test_token")
    assert pm.auth.is_logged_in()
    
    # Add some files
    with open(os.path.join(project_dir, "main.aayu"), "w") as f:
        f.write("print('hello')")
        
    pm.publish()
    
    # Search
    pm.search("project")
    results = pm.registry.search("project")
    assert len(results) == 1
    assert results[0]["name"] == "project"

if __name__ == '__main__':
    pytest.main(['-v', __file__])
