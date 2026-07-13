import sys
import os

# Add local directory to path
sys.path.insert(0, os.path.abspath('..'))

from tools.builder.builder import Builder
builder = Builder()
builder.build("windows")
