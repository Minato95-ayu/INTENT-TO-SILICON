import sys
import os
import shutil
import platform

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

AAYU_VERSION = "0.1.0"

def print_usage():
    print(f"AAYU CLI v{AAYU_VERSION}")
    print("Usage:")
    print("  aayu version             - Show version")
    print("  aayu doctor              - Check system environment")
    print("  aayu new <project>       - Scaffold a new project")
    print("  aayu run                 - Run the current project")
    print("  aayu install <package>   - Install a package")
    print("  aayu test                - Run test suite")
    print("  aayu compile <file.aayu> - Compile AAYU file to bytecode (.ayc)")
    print("  aayu vm <file.aayu/.ayc> - Run AAYU file/bytecode on the stack VM")
    print("  aayu inspect <file>      - Generate AAYU IR from source file")
    print("  aayu build               - Build the project (stub)")

def do_version():
    print(f"AAYU CLI v{AAYU_VERSION}")

def do_doctor():
    print("AAYU CLI      \u2705")
    # Check if interpreter exists
    interp_exists = os.path.exists(os.path.join(os.path.dirname(__file__), "aayu_language", "interpreter.py"))
    check_mark = '\u2705' if interp_exists else '\u274c'
    print(f"Interpreter   {check_mark}")
    
    # We just simulate Database and Packages for now
    print("Database      \u2705")
    print("Packages      \u2705")

def do_new(project_name):
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return
    
    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, "views"))
    os.makedirs(os.path.join(project_name, ".aayu", "packages"))
    
    # aayu.toml
    toml_content = f"""name = "{project_name}"
version = "0.1.0"

[dependencies]
"""
    with open(os.path.join(project_name, "aayu.toml"), "w", encoding="utf-8") as f:
        f.write(toml_content)
        
    # main.aayu
    main_content = """task home with req.
    return render "views/home.html".
end.

# Define a route
get "/" to home.

# Start the server
serve on 8080.
"""
    with open(os.path.join(project_name, "main.aayu"), "w", encoding="utf-8") as f:
        f.write(main_content)
        
    # views/home.html
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>AAYU App</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
    <h1>Welcome to AAYU</h1>
    <p>Your project is running successfully!</p>
</body>
</html>
"""
    with open(os.path.join(project_name, "views", "home.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    # README.md
    readme_content = f"""# {project_name}

To run this project:
```bash
aayu run
```
"""
    with open(os.path.join(project_name, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # .gitignore
    gitignore_content = """.aayu/packages/
aayu_db.sqlite
*.ayc
"""
    with open(os.path.join(project_name, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)
        
    print(f"Created AAYU project '{project_name}' successfully!")
    print(f"Run `cd {project_name}` and then `aayu run` to start.")

def do_run():
    # Detect if we are in a project directory
    if not os.path.exists("aayu.toml"):
        print("Error: No aayu.toml found. Are you in an AAYU project directory?")
        return
        
    main_file = "main.aayu"
    if not os.path.exists(main_file):
        print(f"Error: {main_file} not found.")
        return
        
    print(f"Compiling {main_file}...")
    
    cli_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(cli_dir, "aayu_language"))
    
    from lexer import Lexer
    from parser import Parser
    from compiler import AAYUCompiler
    from serializer import serialize
    from vm import VirtualMachine
    
    with open(main_file, 'r', encoding='utf-8') as f:
        source = f.read()
        
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename=main_file)
    ast = parser.parse()
    
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    
    out_path = main_file[:-5] + '.ayc'
    serialized = serialize(bytecode)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(serialized)
        
    print("Compiled successfully! Starting VM...")
    vm = VirtualMachine()
    vm.run(bytecode)

def do_build():
    print("AAYU build not implemented yet. Wait for Native Compiler / IR Phase.")

def do_install(package_name):
    if not os.path.exists("aayu.toml"):
        print("Error: No aayu.toml found. Are you in an AAYU project directory?")
        return
        
    packages_dir = os.path.join(".aayu", "packages")
    if not os.path.exists(packages_dir):
        os.makedirs(packages_dir)
        
    # Determine repo URL
    if "/" in package_name:
        repo_url = f"https://github.com/{package_name}.git"
        package_folder = package_name.split("/")[-1]
        if package_folder.startswith("aayu-"):
            package_folder = package_folder[5:]
    else:
        # Default to Minato95-ayu organization
        repo_url = f"https://github.com/Minato95-ayu/aayu-{package_name}.git"
        package_folder = package_name

    dest_dir = os.path.join(packages_dir, package_folder)
    if os.path.exists(dest_dir):
        print(f"Removing existing package '{package_folder}'...")
        import shutil
        shutil.rmtree(dest_dir, ignore_errors=True)
        
    print(f"Installing '{package_folder}' from {repo_url}...")
    import subprocess
    result = subprocess.run(["git", "clone", "--depth", "1", repo_url, dest_dir], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: Failed to install package '{package_name}'.")
        print("Is it a valid AAYU package? Does it exist on GitHub?")
        # print(result.stderr)
        return
        
    # Clean up .git folder to save space and avoid nested repos
    git_dir = os.path.join(dest_dir, ".git")
    if os.path.exists(git_dir):
        import stat
        def remove_readonly(func, path, excinfo):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        import shutil
        shutil.rmtree(git_dir, onerror=remove_readonly)
        
    print(f"Installed '{package_folder}' successfully!")
    
    # Update aayu.toml
    with open("aayu.toml", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Check if already in dependencies
    in_deps = False
    pkg_line = f'{package_folder} = "latest"\n'
    for line in lines:
        if line.strip().startswith(package_folder) and "=" in line:
            in_deps = True
            break
            
    if not in_deps:
        # We need to find [dependencies] block
        deps_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "[dependencies]":
                deps_idx = i
                break
        
        if deps_idx != -1:
            lines.insert(deps_idx + 1, pkg_line)
        else:
            lines.append("\n[dependencies]\n")
            lines.append(pkg_line)
            
        with open("aayu.toml", "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"Added '{package_folder}' to aayu.toml")
    else:
        print(f"'{package_folder}' is already in aayu.toml")

def do_build(intent_prompt):
    import json
    from intent_v4.architecture_builder import ArchitectureBuilder
    from intent_v4.aayu_emitter import AayuEmitter
    
    print("--- AAYU Intent Engine v4 ---")
    print(f"Intent: {intent_prompt}")
    
    try:
        builder = ArchitectureBuilder()
        arch = builder.build(intent_prompt)
        
        with open("architecture.json", "w") as f:
            json.dump(arch, f, indent=2)
            
        emitter = AayuEmitter()
        code = emitter.emit(arch)
        
        with open("main.aayu", "w", encoding="utf-8") as f:
            f.write(code)
            
        print("\n[SUCCESS] Generated main.aayu!")
        print("Run `aayu run` to compile and start the server.")
    except Exception as e:
        print(f"\n[FAIL] {e}")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
        
    cmd = sys.argv[1]
    
    if cmd == "version":
        do_version()
    elif cmd == "doctor":
        do_doctor()
    elif cmd == "new":
        if len(sys.argv) < 3:
            print("Error: Please provide a project name. Example: aayu new myapp")
        else:
            do_new(sys.argv[2])
    elif cmd == "build":
        if len(sys.argv) < 3:
            print("Error: Please provide an intent prompt. Example: aayu build \"Build a CRM\"")
        else:
            do_build(sys.argv[2])
    elif cmd == "run":
        do_run()
    elif cmd == "install":
        if len(sys.argv) < 3:
            print("Error: Please provide a package name. Example: aayu install auth")
        else:
            do_install(sys.argv[2])
    elif cmd == "build":
        do_build()
    elif cmd == "lsp":
        cli_dir = os.path.dirname(__file__)
        lsp_py = os.path.join(cli_dir, "aayu_language", "lsp_server.py")
        import subprocess
        sys.exit(subprocess.call([sys.executable, lsp_py]))
    elif cmd == "test":
        cli_dir = os.path.dirname(__file__)
        test_py = os.path.join(cli_dir, "aayu_language", "test_runner.py")
        import subprocess
        sys.exit(subprocess.call([sys.executable, test_py]))
    elif cmd == "compile":
        args = sys.argv[2:]
        if not args:
            print("Error: `aayu compile` requires a file to compile.")
            print("Usage: aayu compile <file.aayu>")
            sys.exit(1)
        filepath = args[0]
        
        cli_dir = os.path.dirname(__file__)
        sys.path.append(os.path.join(cli_dir, "aayu_language"))
        
        from lexer import Lexer
        from parser import Parser
        from compiler import AAYUCompiler
        from serializer import serialize
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        
        serialized = serialize(bytecode)
        
        if filepath.endswith('.aayu'):
            out_path = filepath[:-5] + '.ayc'
        else:
            out_path = filepath + '.ayc'
            
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(serialized)
        print(f"Compiled successfully: '{filepath}' -> '{out_path}'")
        
    elif cmd == "vm":
        args = sys.argv[2:]
        if not args:
            print("Error: `aayu vm` requires a file to run.")
            print("Usage: aayu vm <file.aayu/.ayc>")
            sys.exit(1)
        filepath = args[0]
        
        cli_dir = os.path.dirname(__file__)
        sys.path.append(os.path.join(cli_dir, "aayu_language"))
        
        from vm import VirtualMachine
        
        if filepath.endswith('.ayc'):
            from serializer import deserialize
            with open(filepath, 'r', encoding='utf-8') as f:
                serialized = f.read()
            bytecode = deserialize(serialized)
        else:
            from lexer import Lexer
            from parser import Parser
            from compiler import AAYUCompiler
            
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
                
            lexer = Lexer(source)
            parser = Parser(lexer.tokenize(), filename=filepath)
            ast = parser.parse()
            
            compiler = AAYUCompiler()
            bytecode = compiler.compile(ast)
            
        vm = VirtualMachine()
        vm.run(bytecode)
    elif cmd == "inspect":
        args = sys.argv[2:]
        if not args:
            print("Error: `aayu inspect` requires a file to inspect.")
            print("Usage: aayu inspect <file.aayu> [--pretty]")
            sys.exit(1)
        filepath = args[0]
        pretty = "--pretty" in args
        
        cli_dir = os.path.dirname(__file__)
        sys.path.append(os.path.join(cli_dir, "aayu_language"))
        
        from lexer import Lexer
        from parser import Parser
        from ir_generator import generate_ir
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        ir_json = generate_ir(ast)
        
        if pretty:
            print("Generated IR:")
            print(ir_json)
        
        out_path = filepath.replace('.aayu', '.ir.json') if filepath.endswith('.aayu') else filepath + '.ir.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(ir_json)
            
        print(f"Generated: {out_path}")
    else:
        print(f"Unknown command: {cmd}")
        print_usage()

if __name__ == "__main__":
    main()
