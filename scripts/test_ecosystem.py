"""
=============================================================================
FILE: test_ecosystem.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import shutil

# Copy aayu-http
shutil.copytree('official_packages/aayu-http', 'apm-test/.aayu/packages/http', dirs_exist_ok=True)
# Copy aayu-gemini
shutil.copytree('official_packages/aayu-gemini', 'apm-test/.aayu/packages/gemini', dirs_exist_ok=True)

with open('apm-test/main.aayu', 'w', encoding='utf-8') as f:
    f.write('''use http.

task main.
    res is get_request("https://jsonplaceholder.typicode.com/todos/1").
    body is get "body" from res.
    title is get "title" from body.
    return title.
end.
''')
