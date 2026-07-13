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
        syntax: "pip install aayu-lang",
        examples: [
          {
            code: "aayu --version\naayu doctor",
            output: "AAYU v1.0.0-stable\nEnvironment checks passed.",
            explanation: "Verify that the installation was successful."
          }
        ],
        bestPractices: [
          "Ensure Python 3.9+ is installed.",
          "Use 'aayu doctor' if commands fail."
        ],
        commonErrors: [
          {
            error: "Command 'aayu' not found",
            fix: "Ensure your Python Scripts directory is added to your PATH environment variable."
          }
        ],
        reference: "For Windows installation, you can also download the standalone .exe from the Releases page."
      },
      {
        slug: "quick-start",
        title: "Quick Start",
        introduction: "Create your first AAYU project and understand the basic compilation and execution cycle.",
        syntax: "aayu new hello_world\ncd hello_world\naayu run",
        examples: [
          {
            code: "app hello_world\n\npage Home\n    text \"Welcome to AAYU\"\nend\n\nrun",
            output: "Welcome to AAYU",
            explanation: "The entry point executes and renders the declarative UI tree."
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
          },
          {
            error: "Unexpected token '-'",
            fix: "Application names cannot contain hyphens. Use underscores (e.g., hello_world instead of hello-world)."
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
        introduction: "AAYU uses a clean, declarative syntax focused on intent. No JSX, no HTML, no CSS spaghetti.",
        syntax: "app my_app\n\n# declarations\n\nrun",
        examples: [
          {
            code: "state count = 0\nstate name = \"Alice\"",
            explanation: "Variables that drive UI are declared with the 'state' keyword."
          }
        ],
        bestPractices: [
          "Use 4-space indentation for readability."
        ],
        commonErrors: [
          {
            error: "SyntaxError: Expected 'end'",
            fix: "Ensure you close all blocks (page, action, row, column, container) with the 'end' keyword."
          }
        ]
      },
      {
        slug: "state",
        title: "State Management",
        introduction: "State management in AAYU is automatic. When a state variable changes, any widget using that state automatically updates.",
        syntax: "state variableName = value",
        examples: [
          {
            code: "state counter = 0\n\naction increment()\n    counter = counter + 1\nend",
            explanation: "Modify state variables inside action blocks."
          }
        ],
        bestPractices: [
          "Group related state at the top of your file."
        ],
        commonErrors: [
          {
            error: "Variable not found",
            fix: "Make sure state variables are declared before they are used."
          }
        ]
      }
    ]
  },
  {
    title: "Widget Catalog",
    items: [
      {
        slug: "text",
        title: "Text",
        introduction: "Displays a string of text or a state variable on the screen.",
        syntax: "text \"String Literal\" OR text state_variable",
        examples: [
          {
            code: "text \"Hello World\"",
            output: "Hello World"
          }
        ],
        bestPractices: ["Use text widgets for rendering static data or variables directly."],
        commonErrors: []
      },
      {
        slug: "button",
        title: "Button",
        introduction: "A clickable button that triggers an action.",
        syntax: "button \"Label\" onClick=\"actionName\"",
        examples: [
          {
            code: "button \"Submit\" onClick=\"submitAction\"",
            explanation: "Triggers the 'submitAction' block when clicked."
          }
        ],
        bestPractices: ["Always provide an onClick handler for interactive buttons."],
        commonErrors: []
      }
    ]
  },
  {
    title: "Tooling",
    items: [
      {
        slug: "cli",
        title: "Command Line Interface",
        introduction: "The AAYU CLI is your primary interface for interacting with the language. It provides tools for compiling, running, and managing your projects.",
        syntax: "aayu <command> [options]",
        examples: [
          {
            code: "aayu run\naayu new <project_name>\naayu build\naayu doctor\naayu disassemble",
            explanation: "Core commands for the development lifecycle."
          }
        ],
        bestPractices: [
          "Use 'aayu doctor' to troubleshoot environment issues."
        ],
        commonErrors: []
      }
    ]
  }
];

export function getDocItem(slug: string): DocItem | undefined {
  for (const section of documentationData) {
    const item = section.items.find(i => i.slug === slug);
    if (item) return item;
  }
  return undefined;
}