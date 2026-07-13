import os
import tempfile
import zipfile
from .manifest import Manifest
from .security import SecurityInfo

class Publisher:
    """Packages a local project and publishes to the registry."""
    
    def __init__(self, registry):
        self.registry = registry
        
    def publish(self, project_dir: str):
        manifest_path = os.path.join(project_dir, "aayu.json")
        manifest = Manifest.load(manifest_path)
        
        # Zip the contents, excluding .aayu_modules and aayu.lock
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, f"{manifest.name}.zip")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(project_dir):
                    if '.aayu_modules' in dirs:
                        dirs.remove('.aayu_modules')
                        
                    for file in files:
                        if file == "aayu.lock":
                            continue
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, project_dir)
                        zf.write(file_path, arcname)
                        
            # Update manifest with checksum
            checksum = SecurityInfo.generate_checksum(zip_path)
            manifest.data["checksum"] = checksum
            manifest.save()
            
            # Send to registry
            self.registry.publish(manifest.data, zip_path)
            return manifest.name, manifest.version
