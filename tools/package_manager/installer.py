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
            self._validate_archive(zip_ref, target_dir)
            zip_ref.extractall(target_dir)
            
        # Optional: Run postinstall hooks here
        return True

    @staticmethod
    def _validate_archive(zip_ref: zipfile.ZipFile, target_dir: str) -> None:
        """Reject archive members that can escape the package directory."""
        target_root = os.path.realpath(target_dir)
        for member in zip_ref.infolist():
            member_path = os.path.realpath(os.path.join(target_root, member.filename))
            if os.path.commonpath((target_root, member_path)) != target_root:
                raise ValueError(f"Package archive contains an unsafe path: {member.filename}")

            mode = (member.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                raise ValueError(f"Package archive contains an unsafe symlink: {member.filename}")
        
    def remove(self, name: str):
        target_dir = os.path.join(self.modules_dir, name)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            return True
        return False
