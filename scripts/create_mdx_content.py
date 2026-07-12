import os

docs_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\content\docs'

# Structure: docs / <section> / <slug>.mdx
structure = {
    "getting-started": {
        "installation.mdx": '''---
title: "Installation"
description: "How to install the AAYU Compiler and BrainOS CLI."
order: 1
---

# Installation

Welcome to AAYU. You can install the AAYU toolchain using our official installer or build from source.

## Pre-built Binaries (Coming in v1.0)
Currently, AAYU is in internal preview. Once public, you will be able to run:

<CodeBlock lang="bash" code="curl -fsSL https://aayu.dev/install.sh | bash" />

## Build from Source
If you have access to the repository, you can build AAYU locally:

<CodeBlock lang="bash" code="git clone https://github.com/aayu/aayu.git\\ncd aayu\\nmake build" />

## Verifying Installation
Verify your installation by checking the version:

<CodeBlock lang="bash" code="aayu --version" />

<PageNav next={{title: "Hello World", href: "/docs/getting-started/hello-world"}} />
''',
        "hello-world.mdx": '''---
title: "Hello World"
description: "Your first AAYU program."
order: 2
---

# Hello World

Let's write your first program in AAYU. 

AAYU files end with the .aayu extension. Create a file named main.aayu and add the following:

<CodeBlock lang="aayu" code='fn main()\\ndo\\n    print("Hello, World!").\\nend.' playgroundUrl="/playground" />

## Running the Program

Run the program using the AAYU CLI:

<CodeBlock lang="bash" code="aayu run main.aayu" />

<PageNav prev={{title: "Installation", href: "/docs/getting-started/installation"}} next={{title: "Syntax", href: "/docs/language/syntax"}} />
'''
    },
    "language": {
        "syntax.mdx": '''---
title: "Syntax"
description: "Understanding AAYU's keyword-driven syntax."
order: 1
---

# Syntax Basics

AAYU uses a clean, keyword-driven syntax. Unlike C or Java, statements are terminated with a period (.).

## Entity Declarations
Entities are the core structs in AAYU. They hold state.

<CodeBlock lang="aayu" code="entity User\\nhas\\n    name: Text\\n    age: Number\\nend." playgroundUrl="/playground" />

## Common Errors
A frequent mistake for beginners is forgetting the terminating period.

<ErrorBlock 
    wrong="entity User\\nhas\\n    name: Text\\nend"
    correct="entity User\\nhas\\n    name: Text\\nend."
    errorMsg="SyntaxError: Expected '.' at the end of declaration block."
/>

<PageNav prev={{title: "Hello World", href: "/docs/getting-started/hello-world"}} />
'''
    }
}

for section, files in structure.items():
    section_dir = os.path.join(docs_dir, section)
    os.makedirs(section_dir, exist_ok=True)
    for filename, content in files.items():
        with open(os.path.join(section_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)

print("Created MDX content structure.")
