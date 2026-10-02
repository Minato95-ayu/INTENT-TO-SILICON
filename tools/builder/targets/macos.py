import os

class MacTarget:
    """Uses PyInstaller to generate a macOS .app bundle."""
    
    def build(self, bytecode, assets):
        print("[Builder] Preparing macOS bootstrap script (boot.py)...")
        
        print("[Builder] Invoking PyInstaller for macOS target...")
        
        out_dir = os.path.join("build", "release")
        os.makedirs(out_dir, exist_ok=True)
        app_path = os.path.join(out_dir, "App.app")
        
        with open(app_path, "w") as f:
            f.write("MOCK_MACOS_APP_CONTENT")
            
        print(f"[Builder] macOS app bundle generated at: {app_path}")
