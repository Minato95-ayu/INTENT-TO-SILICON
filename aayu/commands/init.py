import os
import sys
from aayu.package.manifest import AayuManifest

def handle(args):
    # Initialize in current directory
    project_dir = os.getcwd()
    project_name = os.path.basename(project_dir)
    
    toml_path = os.path.join(project_dir, "Aayu.toml")
    json_path = os.path.join(project_dir, "aayu.json")
    
    if os.path.exists(toml_path):
        print("Error: Aayu.toml already exists in this directory.")
        sys.exit(1)
        
    if os.path.exists(json_path):
        print("Warning: aayu.json found. Consider running 'aayu migrate' instead.")
        
    # Check if there is a main file
    entry_point = "src/main.aayu"
    if not os.path.exists(os.path.join(project_dir, "src")):
        if os.path.exists(os.path.join(project_dir, "main.aayu")):
            entry_point = "main.aayu"
        elif os.path.exists(os.path.join(project_dir, "app.aayu")):
            entry_point = "app.aayu"
            
    with open(toml_path, "w") as f:
        f.write(AayuManifest.create_default(project_name, entry_point))
        
    print(f"Initialized new AAYU project in {project_dir}")
