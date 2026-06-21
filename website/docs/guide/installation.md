# Installation

AAYU is designed to run everywhere Python runs. You can use the raw AAYU Interpreter scripts, or install the compiled CLI globally.

## Prerequisites
- Python 3.10+
- SQLite3 (Included in Python)

## Option 1: Global Installation (Recommended)
You can install AAYU directly via npm (Node.js) or Pip:
```bash
npm install -g aayu-cli
# or
pip install aayu-lang
```

Once installed, verify the CLI:
```bash
aayu --version
```

## Option 2: Clone the Repository
If you want to contribute to the language internals, or build the core yourself:
```bash
git clone https://github.com/aayu-lang/aayu.git
cd aayu/prototype
python cli.py run myapp.aayu
```

## Next Steps
Now that you have AAYU installed, let's write your first program! Head over to the [Hello World](/guide/hello-world) guide.
