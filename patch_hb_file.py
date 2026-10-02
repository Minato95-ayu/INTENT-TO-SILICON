import re

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_sec = """# 1. File I/O (Native)
let text = file::read("data.txt")
file::write("log.txt", "Server started")"""

new_sec = """# 1. File I/O (Native)
file::write("data.txt", "Hello AAYU")
let text = file::read("data.txt")"""

text = text.replace(old_sec, new_sec)

with open('AAYU_LANGUAGE_HANDBOOK_V1.md', 'w', encoding='utf-8') as f:
    f.write(text)
