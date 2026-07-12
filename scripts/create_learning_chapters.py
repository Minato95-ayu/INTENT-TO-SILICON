import os

base_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\learning'
os.makedirs(base_dir, exist_ok=True)

chapters = [
    ("00-how-aayu-works.md", "# How AAYU Works\n\nWelcome to the AAYU Compiler learning path! AAYU is designed as a self-teaching codebase. The pipeline is:\n\nSource Code -> Lexer -> Parser -> AST -> Semantic Analysis -> Compiler -> Bytecode -> VM\n\nStart your journey with [01-lexer.md](./01-lexer.md)."),
    ("01-lexer.md", "# 1. Lexer\n\nThe Lexer converts raw text into a stream of tokens.\n\nCode link: [prototype/language/lexer.py](../prototype/language/lexer.py)\n\nNext: [02-parser.md](./02-parser.md)"),
    ("02-parser.md", "# 2. Parser\n\nThe Parser takes tokens and groups them into an Abstract Syntax Tree (AST) representing the logical structure of your code.\n\nCode link: [prototype/language/parser.py](../prototype/language/parser.py)\n\nNext: [03-ast.md](./03-ast.md)"),
    ("03-ast.md", "# 3. Abstract Syntax Tree (AST)\n\nAST Nodes define the objects that the Parser builds (e.g., EntityNode, FunctionNode).\n\nCode link: [prototype/language/ast_nodes.py](../prototype/language/ast_nodes.py)\n\nNext: [04-semantic.md](./04-semantic.md)"),
    ("04-semantic.md", "# 4. Semantic Analyzer\n\nEnforces type safety, scoping, and validates Trait implementations.\n\nCode link: [prototype/language/passes/semantic/type_checker.py](../prototype/language/passes/semantic/type_checker.py)\n\nNext: [05-compiler.md](./05-compiler.md)"),
    ("05-compiler.md", "# 5. Compiler\n\nThe Compiler lowers the validated AST into executable instructions (Bytecode or LLVM IR).\n\nCode link: [prototype/language/compiler.py](../prototype/language/compiler.py)\n\nNext: [06-bytecode.md](./06-bytecode.md)"),
    ("06-bytecode.md", "# 6. Bytecode ISA\n\nThe instruction set architecture for the AAYU Virtual Machine.\n\nCode link: [prototype/language/bytecode.py](../prototype/language/bytecode.py)\n\nNext: [07-runtime.md](./07-runtime.md)"),
    ("07-runtime.md", "# 7. Virtual Machine (Runtime)\n\nThe loop that executes AAYU bytecode instructions.\n\nCode link: [prototype/language/runtime/vm/vm.py](../prototype/language/runtime/vm/vm.py)\n\nNext: [08-memory.md](./08-memory.md)"),
    ("08-memory.md", "# 8. Memory Manager\n\nHow AAYU manages the heap using Deterministic ARC.\n\nCode link: [prototype/language/runtime/memory/manager.py](../prototype/language/runtime/memory/manager.py)\n\nNext: [09-package-manager.md](./09-package-manager.md)"),
    ("09-package-manager.md", "# 9. Package Manager\n\nHow workspaces, modules, and ayu.mod files are resolved.\n\nCode link: [prototype/language/workspace/workspace.py](../prototype/language/workspace/workspace.py)\n\nNext: [10-brainos.md](./10-brainos.md)"),
    ("10-brainos.md", "# 10. BrainOS Orchestrator\n\nThe autonomous AI architect that guides the Intent pipeline.\n\nCode link: [prototype/brainos/orchestrator.py](../prototype/brainos/orchestrator.py)\n\nNext: [11-intent-engine.md](./11-intent-engine.md)"),
    ("11-intent-engine.md", "# 11. Intent Engine\n\nHow NLP and Knowledge Bases are converted into an Intent Graph.\n\nCode link: [prototype/intent_engine/pipeline.py](../prototype/intent_engine/pipeline.py)\n\nEnd of core learning path!")
]

for filename, content in chapters:
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)

print("Created 12 learning chapters in learning/ directory.")
