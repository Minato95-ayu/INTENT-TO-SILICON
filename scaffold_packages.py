import os

base = 'D:/intent-to-silicon-research/INTENT-TO-SILICON/official_packages'
os.makedirs(base, exist_ok=True)

for pkg in ['aayu-auth', 'aayu-http', 'aayu-gemini', 'aayu-email', 'aayu-upload']:
    path = os.path.join(base, pkg)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'aayu.toml'), 'w', encoding='utf-8') as f:
        f.write(f'[package]\nname = "{pkg}"\nversion = "0.1.0"\n')
    with open(os.path.join(path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f'# {pkg}\n\nOfficial AAYU package for {pkg.split("-")[1]}.\n')
    with open(os.path.join(path, 'main.aayu'), 'w', encoding='utf-8') as f:
        f.write(f'# {pkg} main module\n')
