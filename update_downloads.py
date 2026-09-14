import re

with open("website/app/download/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Make the download explicit for exe and other formats
old_windows = '<Download className="w-4 h-4" /> Download for Windows'
new_windows = '<Download className="w-4 h-4" /> Download Windows (.exe)'

old_mac = '<Monitor className="w-4 h-4 text-zinc-500 shrink-0" /> macOS (Apple Silicon / Intel)'
new_mac = '<Monitor className="w-4 h-4 text-zinc-500 shrink-0" /> macOS (.pkg Installer / Apple Silicon & Intel)'

old_linux = '<Terminal className="w-4 h-4 text-zinc-500 shrink-0" /> Linux (x86_64 / aarch64)'
new_linux = '<Terminal className="w-4 h-4 text-zinc-500 shrink-0" /> Linux (.sh / x86_64 & aarch64)'

if old_windows in content:
    content = content.replace(old_windows, new_windows)
if old_mac in content:
    content = content.replace(old_mac, new_mac)
if old_linux in content:
    content = content.replace(old_linux, new_linux)

with open("website/app/download/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated download page")
