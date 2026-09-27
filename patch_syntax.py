with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("file::read", "file.read")
text = text.replace("file::write", "file.write")
text = text.replace("file::delete", "file.delete")

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(text)

with open("runtime/stdlib/modules/file_lib.py", "r", encoding="utf-8") as f:
    text2 = f.read()

text2 = text2.replace("file::read", "file.read")
text2 = text2.replace("file::write", "file.write")
text2 = text2.replace("file::delete", "file.delete")

with open("runtime/stdlib/modules/file_lib.py", "w", encoding="utf-8") as f:
    f.write(text2)

print("Patched :: to . for file I/O!")
