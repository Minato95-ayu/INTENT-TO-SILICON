import os
import shutil
import zipfile
from .security import SecurityInfo
from .exceptions import ChecksumMismatchError

class Installer:
    """Handles physical installation of packages into .aayu_modules."""
    
    def __init__(self, modules_dir: str):
        self.modules_dir = modules_dir
        os.makedirs(self.modules_dir, exist_ok=True)
        
    def install(self, name: str, zip_path: str, expected_checksum: str):
        # 1. Verify Checksum
        if expected_checksum:
            if not SecurityInfo.verify_checksum(zip_path, expected_checksum):
                raise ChecksumMismatchError(f"Checksum validation failed for {name}")
                
        # 2. Unzip to .aayu_modules/name
        target_dir = os.path.join(self.modules_dir, name)
        
        # Clean existing
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
            
        # Optional: Run postinstall hooks here
        return True
        
    def remove(self, name: str):
        target_dir = os.path.join(self.modules_dir, name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            return True
        return False
