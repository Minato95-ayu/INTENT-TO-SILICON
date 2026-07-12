"""
=============================================================================
FILE: base.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os

class BaseGenerator:
    """
    Base class for all AAYU Code Generators.
    Takes the AAYU IR and scaffolds the corresponding target project.
    """
    def __init__(self, ir_data: dict, output_dir: str):
        self.ir = ir_data
        self.output_dir = output_dir

    def ensure_dir(self, path: str):
        full_path = os.path.join(self.output_dir, path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def write_file(self, path: str, content: str):
        full_path = os.path.join(self.output_dir, path)
        # Ensure parent dir exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    def generate(self):
        """Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate()")
