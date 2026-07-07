import os
import re

repo = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

def replace_exact(path_suffix, old, new):
    path = os.path.join(repo, path_suffix)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            t = f.read()
        t = t.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)

# 1. lib/mdx.ts
replace_exact('lib/mdx.ts', 'const fullPath = path.join(DOCS_DIR, category, .mdx);', 'const fullPath = path.join(DOCS_DIR, category, ${slug}.mdx);')

# 2. app/examples/page.tsx
replace_exact('app/examples/page.tsx', 'import { Play, Download, ExternalLink, Code2, Copy, FileCode, CheckCircle2, Terminal, ArrowRight, Github, Code, ArrowUpRight, ShieldCheck, HeartPulse, ShoppingCart, MessageSquare, Briefcase, Calculator, ArrowRight, Github, Database } from "lucide-react";', 'import { Play, Download, ExternalLink, Code2, Copy, FileCode, CheckCircle2, Terminal, ArrowRight, GitBranch, Code, ArrowUpRight, ShieldCheck, HeartPulse, ShoppingCart, MessageSquare, Briefcase, Calculator, Database } from "lucide-react";')
replace_exact('app/examples/page.tsx', '<Github', '<GitBranch')
replace_exact('app/examples/page.tsx', 'href={https://github.com/Minato95-ayu/AAYU/tree/main/examples/\}', 'href="https://github.com/Minato95-ayu/AAYU/tree/main/examples/"')

# 3. app/docs/layout.tsx
replace_exact('app/docs/layout.tsx', 'import { Search, ChevronRight, Menu, Github, BookOpen, Code2, Bot, Layers, CheckCircle2, Box } from "lucide-react";', 'import { Search, ChevronRight, Menu, GitBranch, BookOpen, Code2, Bot, Layers, CheckCircle2, Box } from "lucide-react";')
replace_exact('app/docs/layout.tsx', '<Github', '<GitBranch')


# 4. app/brainos/page.tsx
replace_exact('app/brainos/page.tsx', 'className={ bsolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opac...', 'className="absolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opacity-20 bg-blue-500"')
# Regex for brainos because it was mangled
path3 = os.path.join(repo, 'app/brainos/page.tsx')
with open(path3, 'r', encoding='utf-8') as f:
    text3 = f.read()
text3 = re.sub(r'className=\{\s?bsolute top-0 right-0.*?\}', 'className="absolute top-0 right-0 w-64 h-64 blur-[100px] rounded-full opacity-20 bg-blue-500"', text3)
with open(path3, 'w', encoding='utf-8') as f:
    f.write(text3)


# 5. data/language-content.tsx
path7 = os.path.join(repo, 'data/language-content.tsx')
with open(path7, 'r', encoding='utf-8') as f:
    text7 = f.read()
text7 = text7.replace('{"// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0"}', '{// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0}')
text7 = re.sub(r'\{"// aayu\.mod\nmodule my_app 1\.0\.0\nrequire http_server >= 2\.1\.0"\}', '{// aayu.mod\\nmodule my_app 1.0.0\\nrequire http_server >= 2.1.0}', text7)
with open(path7, 'w', encoding='utf-8') as f:
    f.write(text7)

# 6. data/docs.ts
# Since this file has a ton of duplicated syntax errors at the top from a previous replace, let's fix it by extracting the real content.
path6 = os.path.join(repo, 'data/docs.ts')
with open(path6, 'r', encoding='utf-8') as f:
    text6 = f.read()
# We will just rewrite the whole file cleanly.
docs_clean = """
export interface DocItem {
  slug: string;
  title: string;
  introduction: string;
  syntax?: string;
  examples: { code: string; output?: string; explanation?: string }[];
  bestPractices: string[];
  commonErrors: { error: string; fix: string }[];
  reference?: string;
}

export interface DocSection {
  title: string;
  items: DocItem[];
}

export const documentationData: DocSection[] = [
  {
    title: "Getting Started",
    items: [
      {
        slug: "installation",
        title: "Installation",
        introduction: "AAYU is designed to be installed as a single binary with zero external dependencies. It ships with the compiler, runtime, package manager, and formatter built-in.",
        syntax: "curl -sSf https://aayu.dev/install.sh | sh",
        examples: [
          {
            code: "aayu --version",
            output: "AAYU v1.0.0-stable (Offline-First)",
            explanation: "Verify that the installation was successful."
          }
        ],
        bestPractices: [
          "Always add the AAYU bin directory to your system PATH.",
          "Use the official installer script for automated updates."
        ],
        commonErrors: [
          {
            error: "Command 'aayu' not found",
            fix: "Ensure ~/.aayu/bin is added to your PATH environment variable."
          }
        ],
        reference: "For Windows installation, download the standalone .exe from the Releases page."
      },
      {
        slug: "quick-start",
        title: "Quick Start",
        introduction: "Create your first AAYU project and understand the basic compilation and execution cycle.",
        syntax: "aayu new my_project\\ncd my_project\\naayu run main.aayu",
        examples: [
          {
            code: 'print("Hello AAYU from the Intent Engine!").',
            output: "Hello AAYU from the Intent Engine!",
            explanation: "The entry point executes sequentially from top to bottom."
          }
        ],
        bestPractices: [
          "Use 'aayu new' to scaffold projects so the directory structure is standard.",
          "Always compile with 'aayu build' before deploying."
        ],
        commonErrors: [
          {
            error: "Cannot find main.aayu",
            fix: "Ensure you are in the root of the project directory before running."
          }
        ]
      }
    ]
  },
  {
    title: "Language Core",
    items: [
      {
        slug: "syntax",
        title: "Syntax & Basics",
        introduction: "AAYU uses a clean, dot-terminated syntax with significant whitespace avoidance where possible. It prioritizes readability and explicit intent.",
        syntax: "keyword Identifier \\n    body \\nend.",
        examples: [
          {
            code: "let x: Number = 42.\\nlet name: Text = \\"AAYU\\".",
            explanation: "Variables are strongly typed and explicitly declared."
          }
        ],
        bestPractices: [
          "Always terminate top-level declarations with a dot (.).",
          "Use 4-space indentation for readability."
        ],
        commonErrors: [
          {
            error: "SyntaxError: Expected '.' after declaration",
            fix: "Ensure you place a dot at the end of block declarations or top-level statements."
          }
        ]
      },
      {
        slug: "functions",
        title: "Functions",
        introduction: "Functions in AAYU are first-class citizens, strongly typed, and support explicit return semantics.",
        syntax: "fn functionName(arg1: Type) -> ReturnType\\ndo\\n    # implementation\\nend.",
        examples: [
          {
            code: "fn calculateAge(birthYear: Number) -> Number\\ndo\\n    return 2026 - birthYear.\\nend.",
            output: "",
            explanation: "A simple function returning a Number."
          }
        ],
        bestPractices: [
          "Keep functions small and focused on a single intent.",
          "Always explicitly declare return types unless it's a void function."
        ],
        commonErrors: [
          {
            error: "TypeError: Expected Number but got Text",
            fix: "Check your return statement matches the declared return type."
          }
        ]
      }
    ]
  },
  {
    title: "Architecture Components",
    items: [
      {
        slug: "records",
        title: "Records (Entities)",
        introduction: "Records are the primary data structures in AAYU. They represent state and fields. They do not contain logic (methods are added via Extensions).",
        syntax: "entity EntityName\\nhas\\n    fieldName : FieldType\\nend.",
        examples: [
          {
            code: "entity Student\\nhas\\n    name : Text\\n    age : Number\\nend.",
            explanation: "Defines a data model for a Student."
          }
        ],
        bestPractices: [
          "Use singular nouns for Record names (e.g., Student, not Students).",
          "Keep Records strictly as data containers to maintain the Intent Architecture."
        ],
        commonErrors: [
          {
            error: "Property 'age' does not exist on Student",
            fix: "Ensure the field is declared inside the 'has' block of the entity."
          }
        ]
      }
    ]
  },
  {
    title: "Toolchain & CLI",
    items: [
      {
        slug: "cli",
        title: "CLI Reference",
        introduction: "The AAYU CLI is the single entry point for all development operations. It includes the compiler, formatter, linter, and BrainOS interface.",
        syntax: "aayu <command> [options]",
        examples: [
          {
            code: "aayu init my_app",
            explanation: "Scaffolds a new AAYU project with the standard directory structure."
          },
          {
            code: "aayu run main.aayu",
            explanation: "Compiles and immediately executes the script via the VM."
          },
          {
            code: "aayu build src/",
            explanation: "Compiles the source directory into an optimized production binary."
          },
          {
            code: "aayu fmt .",
            explanation: "Formats all AAYU code in the current directory."
          },
          {
            code: "aayu lint",
            explanation: "Runs static analysis and Intent graph validation."
          },
          {
            code: "aayu package install",
            explanation: "Resolves and installs dependencies from AAYU Registry."
          },
          {
            code: "aayu doctor",
            explanation: "Checks environment setup, dependencies, and memory constraints."
          },
          {
            code: "aayu brainos analyze",
            explanation: "Forces the BrainOS engine to output architectural tradeoffs for the current project."
          }
        ],
        bestPractices: [
          "Use 'aayu doctor' whenever you encounter weird environment errors.",
          "Run 'aayu fmt' before committing code to maintain a clean codebase."
        ],
        commonErrors: [
          {
            error: "Error: No BrainOS knowledge base found.",
            fix: "Ensure you are running AAYU inside an initialized project (aayu init) or that the global KB path is set."
          }
        ]
      }
    ]
  }
];

export function getDocItem(slug: string): DocItem | undefined {
  for (const section of documentationData) {
    for (const item of section.items) {
      if (item.slug === slug) {
        return item;
      }
    }
  }
  return undefined;
}
"""
with open(path6, 'w', encoding='utf-8') as f:
    f.write(docs_clean)

