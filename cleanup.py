import os
import shutil

# Items to move to .archive
items_to_archive = [
    "compiler_aayu",
    "bench.c",
    "bench_c.exe",
    "bench_jit.py",
    "benchmark.py",
    "benchmark.aayu",
    "collections_proof.aayu",
    "file_exception_proof.aayu",
    "file_proof.aayu",
    "hello.aybc",
    "hello.exe",
    "lexer_proof.aayu",
    "self_hosting_proof.aayu",
    "string_proof.aayu",
    "string_proof2.aayu",
    "test_fullstack.aayu",
    "test_native.aayu",
    "test_output_aayu.txt",
    "test_parse.aayu",
    "test_syntax.aayu",
    "test_app.js",
    "test_asgi.py",
    "test_uv.py",
    "test_uv.spec",
    "uvicorn_stderr.log",
    "build_entry.py",
    "installer_gui.py",
    "optimize_vm.py",
    "push_exe.py",
    "out.log",
    "patch_lexer.py",
    "patch_lexer2.py",
    "patch_router.py",
    "test_hello.aybc"
]

os.makedirs(".archive", exist_ok=True)

moved = []
for item in items_to_archive:
    if os.path.exists(item):
        dest = os.path.join(".archive", item)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            else:
                os.remove(dest)
        shutil.move(item, ".archive/")
        moved.append(item)

print(f"Archived {len(moved)} items.")
