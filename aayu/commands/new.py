import os
import sys
import shutil
from aayu.package.manifest import AayuManifest

def handle(args):
    if len(args) < 1:
        print("Usage: aayu new <ProjectName> [template]")
        print("Available templates: blank (default), ecommerce, dashboard")
        sys.exit(1)
    
    project_name = args[0]
    template = args[1] if len(args) > 1 else "blank"
    
    # Path to the templates directory
    aayu_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(aayu_dir, "templates", template)
    
    if not os.path.exists(template_dir):
        print(f"Error: Template '{template}' not found.")
        sys.exit(1)
        
    try:
        # Copy the template directory to the new project name
        shutil.copytree(template_dir, project_name)
        
        # Determine entry point based on template (ecommerce/dashboard might use src/main.aayu or similar)
        entry_point = "src/main.aayu" if template == "blank" else "src/app.aayu"
        if not os.path.exists(os.path.join(project_name, "src")):
            # basic heuristic
            if os.path.exists(os.path.join(project_name, "main.aayu")):
                entry_point = "main.aayu"
            elif os.path.exists(os.path.join(project_name, "app.aayu")):
                entry_point = "app.aayu"

        # Create Aayu.toml
        toml_path = os.path.join(project_name, "Aayu.toml")
        if not os.path.exists(toml_path):
            with open(toml_path, "w") as f:
                f.write(AayuManifest.create_default(project_name, entry_point))
                
        # Remove legacy aayu.json if template copied it
        json_path = os.path.join(project_name, "aayu.json")
        if os.path.exists(json_path):
            os.remove(json_path)
                
        print(f"Created new AAYU project '{project_name}' using template '{template}'.")
        print(f"  cd {project_name}")
        print(f"  aayu run")
    except Exception as e:
        print(f"Error creating project: {e}")
        sys.exit(1)
