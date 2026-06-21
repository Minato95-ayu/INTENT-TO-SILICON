from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="aayu-lang",
    version="1.0.0",
    description="AAYU: The Intent-to-Silicon Programming Language - Intent-Driven, Full-Stack Development Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AAYU Team",
    author_email="support@aayu.org",
    url="https://aayu.org",
    project_urls={
        "Repository": "https://github.com/Minato95-ayu/INTENT-TO-SILICON",
        "Documentation": "https://aayu-lang.github.io",
        "Issues": "https://github.com/Minato95-ayu/INTENT-TO-SILICON/issues",
        "Changelog": "https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/CHANGELOG.md",
    },
    package_dir={"": "prototype"},
    packages=find_packages(where="prototype", include=["aayu_language*", "intent_engine*"]),
    py_modules=["cli"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "aayu=cli:main",
        ]
    },
    install_requires=[
        # AAYU core dependencies
        # Add as needed when publishing
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "docs": [
            "vitepress>=1.0",
            "vue>=3.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    license="MIT",
    keywords="programming-language intent-driven web-framework database rbac workflow compiler intent-engine",
)
