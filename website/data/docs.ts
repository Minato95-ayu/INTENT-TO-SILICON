
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
        syntax: "aayu new my_project\ncd my_project\naayu run main.aayu",
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
        syntax: "keyword Identifier \n    body \nend.",
        examples: [
          {
            code: "let x: Number = 42.\nlet name: Text = \"AAYU\".",
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
        syntax: "fn functionName(arg1: Type) -> ReturnType\ndo\n    # implementation\nend.",
        examples: [
          {
            code: "fn calculateAge(birthYear: Number) -> Number\ndo\n    return 2026 - birthYear.\nend.",
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
        syntax: "entity EntityName\nhas\n    fieldName : FieldType\nend.",
        examples: [
          {
            code: "entity Student\nhas\n    name : Text\n    age : Number\nend.",
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
