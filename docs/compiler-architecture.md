# Compiler Architecture

The AAYU compiler is a multi-pass pipeline written in Python (soon porting to Rust).

## 1. Lexer (lexer.py)
Converts raw string input into a stream of semantic Tokens, identifying identifiers, numbers, texts, and structural keywords (let, mut, n).

## 2. Parser (parser.py)
Consumes the token stream and builds an Abstract Syntax Tree (AST). It enforces strict syntactical rules like mandatory periods for statements.

## 3. Semantic Analyzer (semantic.py)
Performs static type checking, scope resolution, and validates symbol definitions.

## 4. Bytecode Generator (compiler.py)
Compiles the validated AST down to a custom AAYU Instruction Set Architecture (ISA), ready for VM execution.\n