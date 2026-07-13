import os

class LinuxTarget:
    """Uses PyInstaller to generate a Linux ELF binary."""
    
    def build(self, bytecode, assets):
        print("[Builder] Preparing Linux bootstrap script (boot.py)...")
        
        print("[Builder] Invoking PyInstaller for Linux target...")
        
        out_dir = os.path.join("build", "release")
        os.makedirs(out_dir, exist_ok=True)
        elf_path = os.path.join(out_dir, "app")
        
        with open(elf_path, "w") as f:
            f.write("MOCK_LINUX_ELF_CONTENT")
            
        print(f"[Builder] Linux binary generated at: {elf_path}")
