with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('("file.write", 2), ("file.delete", 1)', '("file.write", 2), ("file.append", 2), ("file.delete", 1), ("file.exists", 1), ("file.mkdir", 1)')

with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Added file functions")
