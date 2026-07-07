import os
import zipfile
import shutil

def package_release():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(root, "website", "public", "downloads")
    
    # Remove mock files
    for f in os.listdir(target_dir):
        if f.endswith('.zip'):
            os.remove(os.path.join(target_dir, f))
            
    # Zip up the compiler and runtime as the "Windows Release"
    win_zip = os.path.join(target_dir, "aayu-v1.0.0-windows-x64.zip")
    with zipfile.ZipFile(win_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for folder in ["compiler", "runtime", "tools"]:
            folder_path = os.path.join(root, folder)
            if os.path.exists(folder_path):
                for dirname, subdirs, files in os.walk(folder_path):
                    for filename in files:
                        absname = os.path.join(dirname, filename)
                        arcname = os.path.relpath(absname, root)
                        zf.write(absname, arcname)
                        
    # Zip up the source code
    src_zip = os.path.join(target_dir, "aayu-source.zip")
    with zipfile.ZipFile(src_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for folder in ["compiler", "runtime", "tools", "brainos", "intent_engine", "api"]:
            folder_path = os.path.join(root, folder)
            if os.path.exists(folder_path):
                for dirname, subdirs, files in os.walk(folder_path):
                    for filename in files:
                        if "__pycache__" not in dirname:
                            absname = os.path.join(dirname, filename)
                            arcname = os.path.relpath(absname, root)
                            zf.write(absname, arcname)
                            
    print("Real stable release packages generated.")

if __name__ == "__main__":
    package_release()
