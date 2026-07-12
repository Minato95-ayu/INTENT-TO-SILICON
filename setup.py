"""
=============================================================================
FILE: setup.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

# Import required libraries for package setup and file handling
from setuptools import setup, find_packages  # setuptools: used to create Python packages that can be installed via pip
from pathlib import Path  # pathlib: used for working with file paths in a cross-platform way (works on Windows, Mac, Linux)

# ============================================================================
# STEP 1: Read the README.md file to use as the package's long description
# ============================================================================
# This section reads the README.md file to display on PyPI (Python Package Index)
# when someone visits your package page. It helps users understand what AAYU is.
this_directory = Path(__file__).parent  # Get the directory where this file (setup.py) is located
long_description = (this_directory / "README.md").read_text(encoding="utf-8")  # Read the README.md file as text


# ============================================================================
# STEP 2: Configure the Python Package using setup() function
# ============================================================================
# The setup() function tells Python how to install and distribute your package.
# Think of it as an instruction manual for how to properly install AAYU on someone's computer.
setup(
    # Basic package information - shown when installing and on PyPI
    name="aayu-lang",  # The name people use to install: "pip install aayu-lang"
    version="1.0.0",  # Version number (follows semantic versioning: major.minor.patch)
    description="AAYU: The Intent-to-Silicon Programming Language - Intent-Driven, Full-Stack Development Platform",  # Short description
    long_description=long_description,  # The long description is the README.md content we read above
    long_description_content_type="text/markdown",  # Tells PyPI that long_description is in Markdown format
    
    # Author information - lets people know who maintains this package
    author="Ayush Kaushik",  # Your name
    author_email="ayushkaushi1441@gmail.com",  # Your email for support
    
    # URLs where people can find more information about the project
    url="https://github.com/Minato95-ayu/INTENT-TO-SILICON",  # Main project repository
    project_urls={
        "Repository": "https://github.com/Minato95-ayu/INTENT-TO-SILICON",  # Where the code is stored
        "Documentation": "https://aayu-lang.github.io",  # Where to learn how to use AAYU
        "Issues": "https://github.com/Minato95-ayu/INTENT-TO-SILICON/issues",  # Where to report bugs
        "Changelog": "https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/CHANGELOG.md",  # What changed in each version
    },
    
    # ========================================================================
    # STEP 3: Specify which Python code files to include in the package
    # ========================================================================
    package_dir={"": "."},
    packages=find_packages(where=".", include=["compiler*", "runtime*", "tools*", "brainos*", "intent_engine*"]),
    include_package_data=True,
    
    # ========================================================================
    # STEP 4: Create command-line command that users can run
    # ========================================================================
    # This creates a command called "aayu" that users can type in their terminal
    # When they type "aayu", it will run the main() function from the cli module
    entry_points={
        "console_scripts": [
            "aayu=tools.cli:main",  # Creates "aayu" command that calls the main() function from tools.cli
        ]
    },
    
    # ========================================================================
    # STEP 5: Specify package dependencies
    # ========================================================================
    # Dependencies are other Python libraries that your package needs to work
    install_requires=[
        # Currently empty - add packages here as your project grows
        # Example: "requests>=2.28.0" would require the requests library version 2.28 or higher
    ],
    
    # Optional dependencies - only installed if user specifically requests them
    # Users can install these with: "pip install aayu-lang[dev]" or "pip install aayu-lang[docs]"
    extras_require={
        "dev": [  # Development tools - used for testing and code quality
            "pytest>=7.0",  # Testing framework - helps write and run tests
            "pytest-cov>=4.0",  # Code coverage - shows which code is tested
            "black>=23.0",  # Code formatter - makes code look clean and consistent
            "flake8>=6.0",  # Linter - finds code style problems
            "mypy>=1.0",  # Type checker - finds type errors before running code
        ],
        "docs": [  # Documentation tools - used to generate nice documentation
            "vitepress>=1.0",  # Documentation site generator
            "vue>=3.0",  # JavaScript framework for interactive documentation
        ],
    },
    
    # ========================================================================
    # STEP 6: Classify the package on PyPI
    # ========================================================================
    # Classifiers are tags that help people find your package on PyPI
    # They tell PyPI what kind of project this is
    classifiers=[
        "Development Status :: 4 - Beta",  # This is a Beta version (working but may have issues)
        "Environment :: Console",  # This is a command-line tool (runs in terminal)
        "Intended Audience :: Developers",  # This package is for developers
        "License :: OSI Approved :: MIT License",  # Open source license (free to use)
        "Natural Language :: English",  # Documentation is in English
        "Operating System :: OS Independent",  # Works on Windows, Mac, Linux
        "Programming Language :: Python",  # Written in Python
        "Programming Language :: Python :: 3",  # Requires Python 3
        "Programming Language :: Python :: 3.8",  # Tested on Python 3.8
        "Programming Language :: Python :: 3.9",  # Tested on Python 3.9
        "Programming Language :: Python :: 3.10",  # Tested on Python 3.10
        "Programming Language :: Python :: 3.11",  # Tested on Python 3.11
        "Programming Language :: Python :: 3.12",  # Tested on Python 3.12
        "Topic :: Software Development",  # For software developers
        "Topic :: Software Development :: Compilers",  # Has a compiler component
        "Topic :: Software Development :: Interpreters",  # Has an interpreter component
        "Topic :: Internet :: WWW/HTTP",  # Web-related functionality
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",  # Generates dynamic web content
    ],
    
    # ========================================================================
    # STEP 7: Specify minimum Python version and license
    # ========================================================================
    python_requires=">=3.8",  # Requires Python version 3.8 or higher
    license="MIT",  # Using MIT open-source license (free for anyone to use)
    keywords="programming-language intent-driven web-framework database rbac workflow compiler intent-engine",  # Search keywords on PyPI
)
