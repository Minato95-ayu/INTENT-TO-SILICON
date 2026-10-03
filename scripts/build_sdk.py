import os
import shutil
import zipfile
import tarfile
import platform

def build_sdk():
    print("[1/4] Starting AAYU SDK Build Process...")
    
    # Create dist folder
    dist_dir = 'dist'
    sdk_name = 'aayu-sdk'
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(f"{dist_dir}/{sdk_name}/bin", exist_ok=True)
    os.makedirs(f"{dist_dir}/{sdk_name}/lib", exist_ok=True)
    os.makedirs(f"{dist_dir}/{sdk_name}/tools", exist_ok=True)
    
    print("[2/4] Gathering components...")
    
    # 1. Add CLI (aayuc wrapper)
    # We will create a basic executable wrapper script for Windows and Unix
    with open(f"{dist_dir}/{sdk_name}/bin/aayu.bat", "w") as f:
        f.write("@echo off\npython %~dp0..\\tools\\cli.py %*")
    
    with open(f"{dist_dir}/{sdk_name}/bin/aayu", "w") as f:
        f.write("#!/bin/bash\npython3 \\/../tools/cli.py \$@")
    
    # 2. Copy tools, compiler (or self_hosted src)
    if os.path.exists('tools'):
        shutil.copytree('tools', f"{dist_dir}/{sdk_name}/tools", dirs_exist_ok=True)
    if os.path.exists('src'):
        shutil.copytree('src', f"{dist_dir}/{sdk_name}/src", dirs_exist_ok=True)
    
    # 3. Copy Rust VM if built
    vm_path_win = 'runtime_rs/target/release/aayu_vm.exe'
    vm_path_linux = 'runtime_rs/target/release/aayu_vm'
    
    if os.path.exists(vm_path_win):
        shutil.copy(vm_path_win, f"{dist_dir}/{sdk_name}/bin/")
        print(" -> Included Rust VM (Windows)")
    elif os.path.exists(vm_path_linux):
        shutil.copy(vm_path_linux, f"{dist_dir}/{sdk_name}/bin/")
        print(" -> Included Rust VM (Linux/Mac)")
    else:
        print(" -> WARNING: Rust VM not found in release folder. SDK will use fallback mode.")

    print("[3/4] Packaging SDKs for different OS...")
    
    # Create Windows ZIP
    with zipfile.ZipFile(f"{dist_dir}/aayu-windows-amd64-v1.1.0.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(f"{dist_dir}/{sdk_name}"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)
    print(" -> Created aayu-windows-amd64-v1.1.0.zip")
    
    # Create Linux/Mac TAR.GZ
    with tarfile.open(f"{dist_dir}/aayu-linux-mac-v1.1.0.tar.gz", "w:gz") as tar:
        tar.add(f"{dist_dir}/{sdk_name}", arcname=sdk_name)
    print(" -> Created aayu-linux-mac-v1.1.0.tar.gz")
    
    print(f"[4/4] Build Complete! SDKs are ready in the '{dist_dir}' folder.")
    print("These files can now be uploaded to Vercel/GitHub Releases and linked to the website buttons.")

if __name__ == '__main__':
    build_sdk()
