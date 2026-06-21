from setuptools import setup, find_packages

setup(
    name="aayu-lang",
    version="1.0.0",
    description="AAYU: The Intent-to-Silicon Programming Language",
    long_description=open("README.md", "r", encoding="utf-8").read() if open("README.md", "r", encoding="utf-8") else "AAYU Language",
    long_description_content_type="text/markdown",
    author="AAYU Team",
    url="https://aayu.org",
    package_dir={"": "prototype"},
    packages=find_packages(where="prototype", include=["aayu_language*", "intent_engine*"]),
    py_modules=["cli"],
    entry_points={
        "console_scripts": [
            "aayu=cli:main",
        ]
    },
    install_requires=[
        # AAYU dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
