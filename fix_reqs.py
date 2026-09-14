import re

with open("website/app/download/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace LLVM/CMake with Python
old_req = '''              <ul className="text-sm text-zinc-400 space-y-1 ml-8">
                <li>• Modern 64-bit OS (Linux, macOS, Windows via WSL2)</li>
                <li>• C++ compiler — <code className="text-zinc-300 font-mono">clang 14+</code> or <code className="text-zinc-300 font-mono">gcc 12+</code></li>
                <li>• LLVM 17+ (for native code generation)</li>
                <li>• CMake 3.25+ (to build from source)</li>
              </ul>'''

new_req = '''              <ul className="text-sm text-zinc-400 space-y-1 ml-8">
                <li>• Modern 64-bit OS (Linux, macOS, Windows)</li>
                <li>• Python 3.12+ (AAYU Core Engine is currently powered by Python)</li>
                <li>• PIP (Python Package Installer)</li>
              </ul>'''

if old_req in content:
    content = content.replace(old_req, new_req)

old_source_instructions = '''              {[
                "wget /downloads/aayu-source.zip",
                "cd AAYU && cmake -B build -DCMAKE_BUILD_TYPE=Release",
                "cmake --build build --parallel",
              ].map((cmd) => ('''

new_source_instructions = '''              {[
                "git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git",
                "cd INTENT-TO-SILICON",
                "pip install -e .",
              ].map((cmd) => ('''

if old_source_instructions in content:
    content = content.replace(old_source_instructions, new_source_instructions)

with open("website/app/download/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated requirements in download page")
