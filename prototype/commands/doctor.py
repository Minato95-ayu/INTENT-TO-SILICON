import subprocess
import sys

def check_cmd(cmd, name):
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"{name.ljust(12)} \u2713 Installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{name.ljust(12)} \u2717 Missing")
        return False

def run_doctor():
    print("AAYU Environment Diagnostics\n")
    
    python_ok = check_cmd(["python", "--version"], "Python")
    node_ok = check_cmd(["npm", "--version"], "Node.js")
    docker_ok = check_cmd(["docker", "--version"], "Docker")
    git_ok = check_cmd(["git", "--version"], "Git")
    
    print("\nRecommendations:")
    if not node_ok:
        print("- Install Node.js for React Frontend Generation: https://nodejs.org/")
    if not docker_ok:
        print("- Install Docker for Full-Stack Orchestration: https://www.docker.com/")
    if not git_ok:
        print("- Install Git for Version Control: https://git-scm.com/")
        
    if python_ok and node_ok and docker_ok and git_ok:
        print("Your system is fully ready to build AAYU projects! \u2728")
