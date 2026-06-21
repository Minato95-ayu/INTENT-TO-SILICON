import os
import sys

# Mock input function: auth -> yes, payments -> no
answers = ["yes", "no"]
def mock_input(prompt):
    if answers:
        return answers.pop(0)
    return "no"

import builtins
builtins.input = mock_input

from intent_engine import builder
builder.build_app("Build a Job Portal")
