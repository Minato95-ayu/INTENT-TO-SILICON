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

// This data is retained for older internal consumers. The current public docs
// live under content/docs and describe only source-verified behavior.
export const documentationData: DocSection[] = [
  {
    title: "Getting Started",
    items: [
      {
        slug: "installation",
        title: "Build the Rust tools",
        introduction: "AAYU source execution uses the Rust bytecode VM and a separate Rust bootstrap compiler. Both are built from this repository.",
        syntax: "cargo build --release --manifest-path runtime_rs/Cargo.toml\ncargo build --release --manifest-path compiler_bootstrap/Cargo.toml",
        examples: [{
          code: "bin/aayu-vm run tests/test_01_vars.aayu",
          explanation: "Keep aayuc beside the VM or on PATH so the VM can compile source files.",
        }],
        bestPractices: ["Use the Rust VM and bootstrap compiler built from the same checkout."],
        commonErrors: [{
          error: "Compiler (aayuc) not found",
          fix: "Place aayuc beside aayu-vm, in bin/, or on PATH; AAYU_COMPILER_PATH can select an explicit path.",
        }],
        reference: "The VM build command emits .ayc bytecode, not a standalone native executable.",
      },
      {
        slug: "quick-start",
        title: "Quick Start",
        introduction: "The verified starter subset includes variables, arithmetic, conditions, loops, and print.",
        syntax: "let count = 0\nwhile count < 3\n    print(count)\n    count = count + 1\nend",
        examples: [{
          code: "let count = 0\nwhile count < 3\n    print(count)\n    count = count + 1\nend",
          output: "0\n1\n2",
        }],
        bestPractices: ["Run examples with the compiler and VM from the same build."],
        commonErrors: [{
          error: "A module import is rejected",
          fix: "User-defined actions work with positional parameters, local frames, returns, and recursion. Module imports are not implemented yet.",
        }],
      },
    ],
  },
];

export function getDocItem(slug: string): DocItem | undefined {
  for (const section of documentationData) {
    const item = section.items.find(i => i.slug === slug);
    if (item) return item;
  }
  return undefined;
}
