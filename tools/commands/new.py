import os
import sys

def handle(args):
    if len(args) < 1:
        print("Usage: aayu new <ProjectName>")
        sys.exit(1)
    
    project_name = args[0]
    app_name = project_name.replace("-", "_")
    try:
        os.makedirs(project_name)
        
        main_aayu = os.path.join(project_name, "main.aayu")
        with open(main_aayu, "w") as f:
            f.write(f'app {app_name}\n\npage Home\n    title "Welcome to {app_name}"\n    text "Your AAYU app is running!"\nend\n\nrun')
            
        aayu_json = os.path.join(project_name, "aayu.json")
        with open(aayu_json, "w") as f:
            f.write('{\n  "name": "' + project_name + '",\n  "version": "1.0.0",\n  "dependencies": {}\n}')
            
        print(f"Created new AAYU project: {project_name}")
        print(f"  cd {project_name}")
        print(f"  aayu run")
    except Exception as e:
        print(f"Error creating project: {e}")
        sys.exit(1)
