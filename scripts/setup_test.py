"""
=============================================================================
FILE: setup_test.py
PURPOSE: Test file - Validates system functionality
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test file - validates system functionality.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os

os.makedirs('apm-test/.aayu/packages/auth', exist_ok=True)

with open('apm-test/.aayu/packages/auth/main.aayu', 'w', encoding='utf-8') as f:
    f.write('task login with req.\n    return "Login Success!".\nend.\n')

with open('apm-test/main.aayu', 'w', encoding='utf-8') as f:
    f.write('use "auth".\nserve on 8081.\nget "/login" to login.\n')
