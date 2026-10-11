import { ChapterData } from "./tutorial-types";

export const chapters: ChapterData[] = [
  {
    slug: "chapter-1",
    num: 1,
    title: "The AAYU Philosophy",
    phase: "Core Logic & Syntax",
    description: "Understanding Intent Computing. Why Ayush created a language from scratch to replace bloated stacks.",
    learningPoints: [
      "What is Intent-to-Silicon computing",
      "Why AAYU exists — the problem with modern stacks",
      "How AAYU differs from Python, JavaScript, and Rust",
      "The 7-stage compiler pipeline overview"
    ],
    content: `## What is AAYU?

AAYU is a **single-file, full-stack programming language** created by **Ayush Ghrit Kaushik**. Instead of using 10 different tools (React, Express, MongoDB, TensorFlow...), you write ONE \`.aayu\` file and get:

- ✅ Database (SQLite built-in)
- ✅ Backend Server (ASGI HTTP)
- ✅ Frontend UI (Widget Tree)
- ✅ AI/ML (Native engine)
- ✅ Charts & Graphs (Chart.js)
- ✅ Game Engine (Canvas)

### The Problem AAYU Solves

Traditional web development looks like this:
\`\`\`
Frontend: React + Webpack + Babel + TypeScript
Backend:  Express + Node.js + middleware
Database: MongoDB/PostgreSQL + ORM + migrations
AI/ML:    Python + PyTorch + NumPy + Pandas
\`\`\`

That's **15+ dependencies** just to build a simple app! AAYU replaces ALL of this:

\`\`\`aayu
app MyApp
model User
    id Int
    name String
end
route "/api/users"
    get
        respond(User.all())
    end
end
Page Home
    Column
        Text("Welcome!")
        Button("Click Me", onClick: doSomething)
    end
end
run Home
\`\`\`

**One file. Zero dependencies. Full stack.**

### The Compiler Pipeline

When you write AAYU code, it goes through 7 stages:

\`\`\`
Source Code (.aayu)
    ↓
[1] Lexer      → Tokens (keywords, identifiers, operators)
    ↓
[2] Parser     → Abstract Syntax Tree (AST)
    ↓
[3] Semantic   → Type checking, scope validation
    ↓
[4] HIR        → High-level IR (simplified AST)
    ↓
[5] MIR        → Mid-level IR (SSA form, optimizations)
    ↓
[6] LIR        → Low-level IR (register allocation)
    ↓
[7] Bytecode   → Stack-based VM instructions
    ↓
[VM] Execute   → Your app runs!
\`\`\`

This is the same architecture used by Java (JVM) and Python (CPython), but AAYU does it with a **much simpler syntax**.`,
    exercise: "Open the AAYU GitHub repo (github.com/Minato95-ayu/INTENT-TO-SILICON) and explore the `compiler/` folder. Can you find the 7 pipeline stages in the code?"
  },
  {
    slug: "chapter-2",
    num: 2,
    title: "Installation & Tooling",
    phase: "Core Logic & Syntax",
    description: "Setting up the VS Code extension, checking the CLI, and running your first terminal commands.",
    learningPoints: [
      "How to clone and install AAYU",
      "Setting up VS Code with syntax highlighting",
      "Using the AAYU CLI (aayu run, aayu run --web)",
      "Understanding the project structure"
    ],
    content: `## Step 1: Clone the Repository

Open your terminal and run:

\`\`\`bash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
\`\`\`

## Step 2: Install AAYU

AAYU requires Python 3.12+. Install it in development mode:

\`\`\`bash
pip install -e .
\`\`\`

This gives you the \`aayu\` command globally!

## Step 3: Verify Installation

\`\`\`bash
aayu --version
# Output: AAYU v1.1.0 (Intent-to-Silicon)
\`\`\`

## Step 4: VS Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "AAYU" or install from the \`vscode-aayu/\` folder
4. Now \`.aayu\` files get beautiful syntax highlighting! 🎨

## Step 5: Run Your First Program

Create a file called \`hello.aayu\`:

\`\`\`aayu
app Hello
action main
    print("Hello from AAYU!")
end
run main
\`\`\`

Run it:

\`\`\`bash
aayu run hello.aayu
# Output: Hello from AAYU!
\`\`\`

## CLI Commands

| Command | What it does |
|---------|-------------|
| \`aayu run file.aayu\` | Run a program |
| \`aayu run file.aayu --web\` | Run with web server on port 3000 |
| \`aayu compile file.aayu\` | Compile to bytecode only |
| \`aayu --version\` | Show version |`,
    exercise: "Install AAYU on your computer and run `aayu --version`. Take a screenshot of the output!"
  },
  {
    slug: "chapter-3",
    num: 3,
    title: "Hello World in AAYU",
    phase: "Core Logic & Syntax",
    description: "Writing your first AAYU app. Behind the scenes: Lexer to Stack VM compilation explained.",
    learningPoints: [
      "The structure of every AAYU program",
      "What 'app', 'action', 'end', and 'run' mean",
      "How print() works under the hood",
      "Tracing code from source to bytecode"
    ],
    content: `## Your First Program

Every AAYU program starts with the \`app\` keyword:

\`\`\`aayu
app HelloWorld
action main
    print("Hello, World!")
    print("AAYU is amazing!")
end
run main
\`\`\`

Let's break it down line by line:

### Line 1: \`app HelloWorld\`
This **names your application**. Every \`.aayu\` file must start with \`app\`. Think of it like the title of your program.

### Line 2: \`action main\`
An \`action\` is AAYU's word for a **function**. The \`main\` action is special — it's the entry point of your program.

### Line 3-4: \`print("...")\`
\`print()\` is a built-in function that outputs text to the console. You can print strings, numbers, and variables.

### Line 5: \`end\`
Every block in AAYU ends with \`end\`. No curly braces \`{}\` needed!

### Line 6: \`run main\`
This tells AAYU: "Start executing from the \`main\` action." Without this line, nothing happens!

## What Happens Behind the Scenes?

When you run \`aayu run hello.aayu\`, here's what the compiler does:

\`\`\`
Step 1 — LEXER reads your code character by character:
  [APP] [IDENT:HelloWorld] [ACTION] [IDENT:main]
  [IDENT:print] [LPAREN] [STRING:"Hello, World!"] [RPAREN]
  [END] [RUN] [IDENT:main]

Step 2 — PARSER builds a tree:
  AppNode("HelloWorld")
    └─ ActionNode("main")
        └─ CallNode("print", ["Hello, World!"])

Step 3 — BYTECODE GENERATOR creates VM instructions:
  LOAD_CONST  "Hello, World!"
  CALL_FUNC   print, 1
  LOAD_CONST  "AAYU is amazing!"
  CALL_FUNC   print, 1
  HALT

Step 4 — VM EXECUTES the bytecode:
  → Push "Hello, World!" onto stack
  → Pop and print it
  → Push "AAYU is amazing!" onto stack
  → Pop and print it
  → Done!
\`\`\`

## Multiple Actions

You can have multiple actions (functions):

\`\`\`aayu
app Greetings

action sayHello
    print("Hello!")
end

action sayBye
    print("Goodbye!")
end

action main
    sayHello()
    sayBye()
end

run main
\`\`\`

Output:
\`\`\`
Hello!
Goodbye!
\`\`\``,
    exercise: "Write an AAYU program with 3 actions: `greetMorning`, `greetEvening`, and `main`. The `main` action should call both greeting actions."
  },
  {
    slug: "chapter-4",
    num: 4,
    title: "Keywords & Variables",
    phase: "Core Logic & Syntax",
    description: "Deep dive into 'let', dynamic typing, constants, and memory-safe garbage collection.",
    learningPoints: [
      "Declaring variables with 'let'",
      "AAYU's type system: Int, String, Float, Bool",
      "Dynamic typing — variables can change type",
      "How the garbage collector manages memory"
    ],
    content: `## Variables with \`let\`

In AAYU, you create variables using the \`let\` keyword:

\`\`\`aayu
app Variables

action main
    let name = "Ayush"
    let age = 20
    let height = 5.9
    let isStudent = true

    print(name)
    print(age)
    print(height)
    print(isStudent)
end

run main
\`\`\`

Output:
\`\`\`
Ayush
20
5.9
true
\`\`\`

## Data Types

AAYU has 4 basic types:

| Type | Example | Description |
|------|---------|-------------|
| \`Int\` | \`42\` | Whole numbers |
| \`Float\` | \`3.14\` | Decimal numbers |
| \`String\` | \`"hello"\` | Text in quotes |
| \`Bool\` | \`true\`/\`false\` | Yes or No |

## Dynamic Typing

AAYU uses **dynamic typing** — you don't need to specify the type. The compiler figures it out:

\`\`\`aayu
app DynamicTypes

action main
    let x = 10        # x is Int
    print(x)
    
    let x = "hello"   # x is now String!
    print(x)
    
    let x = 3.14      # x is now Float!
    print(x)
end

run main
\`\`\`

## State Variables

For UI-reactive variables, use \`state\` instead of \`let\`:

\`\`\`aayu
app Counter

state count = 0

action increment
    count = count + 1
end

Page Home
    Column
        Text("Count: " + count)
        Button("Add", onClick: increment)
    end
end

run Home
\`\`\`

When \`count\` changes, the UI **automatically updates**! 🔥

## Math Operations

\`\`\`aayu
app Math

action main
    let a = 10
    let b = 3
    
    print(a + b)    # 13 (addition)
    print(a - b)    # 7  (subtraction)
    print(a * b)    # 30 (multiplication)
    print(a / b)    # 3  (division)
    print(a % b)    # 1  (remainder)
end

run main
\`\`\``,
    exercise: "Create a program that calculates the area of a rectangle. Use `let width = 10` and `let height = 5`, then print `width * height`."
  },
  {
    slug: "chapter-5",
    num: 5,
    title: "Loops & Conditions",
    phase: "Core Logic & Syntax",
    description: "Mastering control flow: if, elif, else, and high-performance loop logic in the VM.",
    learningPoints: [
      "if/elif/else conditional blocks",
      "for loops with ranges and lists",
      "while loops for repeated execution",
      "Nested conditions and loops"
    ],
    content: `## If / Elif / Else

Decision making in AAYU:

\`\`\`aayu
app Conditions

action main
    let score = 85

    if score >= 90
        print("Grade: A")
    elif score >= 80
        print("Grade: B")
    elif score >= 70
        print("Grade: C")
    else
        print("Grade: F")
    end
end

run main
\`\`\`

Output: \`Grade: B\`

### Comparison Operators

| Operator | Meaning |
|----------|---------|
| \`==\` | Equal to |
| \`!=\` | Not equal to |
| \`>\` | Greater than |
| \`<\` | Less than |
| \`>=\` | Greater or equal |
| \`<=\` | Less or equal |

## For Loops

Loop through items:

\`\`\`aayu
app Loops

action main
    # Loop with a range
    for i in range(5)
        print(i)
    end
    # Output: 0, 1, 2, 3, 4

    # Loop through a list
    let fruits = ["apple", "banana", "mango"]
    for fruit in fruits
        print("I like " + fruit)
    end
end

run main
\`\`\`

## While Loops

Repeat until a condition is false:

\`\`\`aayu
app WhileLoop

action main
    let count = 0
    while count < 5
        print("Count is: " + count)
        count = count + 1
    end
    print("Done!")
end

run main
\`\`\`

## Nested Example

Combining loops and conditions:

\`\`\`aayu
app Multiplication

action main
    for i in range(1, 11)
        for j in range(1, 11)
            let result = i * j
            if result > 50
                print(i + " x " + j + " = " + result + " (BIG!)")
            end
        end
    end
end

run main
\`\`\``,
    exercise: "Write a program that prints all even numbers from 1 to 20 using a for loop and an if condition."
  },
  {
    slug: "chapter-6",
    num: 6,
    title: "The Built-in SQLite Engine",
    phase: "Database & API",
    description: "Zero-config databases. Defining 'model' schemas, auto-migrations, and data types.",
    learningPoints: [
      "What is a database and why you need one",
      "Defining 'model' blocks for tables",
      "Auto-migration — no setup needed",
      "Column types: Int, String, Float, Bool"
    ],
    content: `## Databases Without Setup

Most languages need you to install a database separately (MySQL, PostgreSQL, MongoDB). In AAYU, the database is **built-in**!

When you define a \`model\`, AAYU automatically:
1. Creates an SQLite database file
2. Creates the table with your columns
3. Handles migrations if you change the schema

Zero config. Zero setup. Just works! ✨

## Defining a Model

\`\`\`aayu
app BlogApp

model Post
    id Int
    title String
    content String
    likes Int = 0
    published Bool = false
end

action main
    print("Blog database ready!")
end

run main
\`\`\`

That's it! AAYU creates a \`Post\` table with 5 columns automatically.

### What Each Line Means:

| Line | Meaning |
|------|---------|
| \`model Post\` | Creates a database table called "Post" |
| \`id Int\` | A number column (auto-incrementing) |
| \`title String\` | A text column |
| \`likes Int = 0\` | Number column with default value 0 |
| \`published Bool = false\` | Boolean column, defaults to false |
| \`end\` | End of model definition |

## Multiple Models

You can have as many models as you want:

\`\`\`aayu
app SocialApp

model User
    id Int
    name String
    email String
end

model Post
    id Int
    content String
    userId Int
end

model Comment
    id Int
    text String
    postId Int
end
\`\`\`

This creates 3 tables: User, Post, and Comment.`,
    exercise: "Create a model called `Student` with columns: id (Int), name (String), grade (Int), and passed (Bool with default true)."
  },
  {
    slug: "chapter-7",
    num: 7,
    title: "CRUD Operations",
    phase: "Database & API",
    description: "Native database querying. Insert, find, update, and delete records instantly.",
    learningPoints: [
      "Creating records with .insert()",
      "Reading records with .all() and .find()",
      "Updating records with .update()",
      "Deleting records with .delete()"
    ],
    content: `## CRUD = Create, Read, Update, Delete

These are the 4 basic database operations. AAYU makes them incredibly simple:

## Create — Insert Records

\`\`\`aayu
app CrudDemo

model Task
    id Int
    title String
    done Bool = false
end

action main
    Task.insert(title: "Learn AAYU", done: false)
    Task.insert(title: "Build an app", done: false)
    Task.insert(title: "Deploy to cloud", done: false)
    
    print("3 tasks created!")
end

run main
\`\`\`

## Read — Get Records

\`\`\`aayu
action showTasks
    # Get ALL records
    let tasks = Task.all()
    print(tasks)

    # Find ONE record by id
    let first = Task.find(1)
    print(first.title)    # "Learn AAYU"
end
\`\`\`

## Update — Modify Records

\`\`\`aayu
action completeTask
    Task.update(1, done: true)
    print("Task 1 completed!")
    
    let task = Task.find(1)
    print(task.done)    # true
end
\`\`\`

## Delete — Remove Records

\`\`\`aayu
action removeTask
    Task.delete(3)
    print("Task 3 removed!")
    
    let remaining = Task.all()
    print(remaining)    # Only 2 tasks left
end
\`\`\`

## Complete Example

\`\`\`aayu
app TodoApp

model Todo
    id Int
    task String
    done Bool = false
end

action main
    # Create
    Todo.insert(task: "Buy groceries")
    Todo.insert(task: "Clean room")
    
    # Read
    let all = Todo.all()
    print("All todos: " + all)
    
    # Update
    Todo.update(1, done: true)
    print("Marked first todo as done!")
    
    # Delete
    Todo.delete(2)
    print("Deleted second todo!")
    
    # Final state
    print("Remaining: " + Todo.all())
end

run main
\`\`\``,
    exercise: "Create a `Contact` model with name and phone. Insert 3 contacts, update one phone number, delete one, and print the remaining contacts."
  },
  {
    slug: "chapter-8",
    num: 8,
    title: "HTTP Server Magic",
    phase: "Database & API",
    description: "Firing up the high-speed ASGI server using the '--web' flag in one command.",
    learningPoints: [
      "Starting the web server with --web flag",
      "How ASGI serves your AAYU app",
      "Understanding port 3000",
      "Serving HTML pages from AAYU"
    ],
    content: `## One Command Web Server

Most frameworks need complex setup to run a web server. AAYU? Just add \`--web\`:

\`\`\`bash
aayu run myapp.aayu --web
\`\`\`

That's it! Your app is now running at **http://localhost:3000** 🚀

## How It Works

When you use \`--web\`, AAYU:
1. Compiles your code to bytecode
2. Starts a high-speed **ASGI** server (like Uvicorn)
3. Renders your Page widgets as HTML
4. Serves them on port 3000
5. Sets up Server-Sent Events for live updates

## Your First Web App

\`\`\`aayu
app WebApp

Page Home
    Column
        Text("Welcome to my website!")
        Text("Built with AAYU 🔥")
        Button("Click me!", onClick: sayHi)
    end
end

action sayHi
    print("Button was clicked!")
end

run Home
\`\`\`

Run it:
\`\`\`bash
aayu run webapp.aayu --web
# Server started at http://localhost:3000
\`\`\`

Open your browser → \`http://localhost:3000\` → See your app! 🎉

## The Widget Tree

AAYU renders your Page as an HTML widget tree:

\`\`\`
Page Home
  └─ Column
      ├─ Text("Welcome...")  → <p> tag
      ├─ Text("Built...")    → <p> tag
      └─ Button("Click")    → <button> tag
\`\`\`

The web renderer converts each widget to proper HTML with styling automatically.

## Server Architecture

\`\`\`
Browser (localhost:3000)
    ↕ HTTP / SSE
AAYU ASGI Server
    ↕ 
Stack VM (executes bytecode)
    ↕
SQLite DB (data storage)
\`\`\``,
    exercise: "Create a web app with a Page that shows your name, age, and a fun fact about you. Run it with `--web` and open it in your browser."
  },
  {
    slug: "chapter-9",
    num: 9,
    title: "REST APIs & Routes",
    phase: "Database & API",
    description: "Creating 'route' blocks, handling GET/POST, and structuring JSON API responses.",
    learningPoints: [
      "What is a REST API",
      "Creating route blocks with GET/POST",
      "Responding with JSON data",
      "Connecting routes to database models"
    ],
    content: `## What is a REST API?

A REST API lets other apps talk to your server. For example:
- \`GET /api/posts\` → Returns all posts
- \`POST /api/posts\` → Creates a new post
- \`GET /api/posts/1\` → Returns post #1

## Creating Routes in AAYU

\`\`\`aayu
app BlogAPI

model Post
    id Int
    title String
    content String
end

route "/api/posts"
    get
        let posts = Post.all()
        respond(posts)
    end
    
    post
        let title = request.body.title
        let content = request.body.content
        Post.insert(title: title, content: content)
        respond({"status": "created"})
    end
end

run main
\`\`\`

Now run with \`--web\`:
\`\`\`bash
aayu run blog.aayu --web
\`\`\`

Test your API:
\`\`\`bash
# Get all posts
curl http://localhost:3000/api/posts

# Create a post
curl -X POST http://localhost:3000/api/posts \\
  -H "Content-Type: application/json" \\
  -d '{"title":"My First Post","content":"Hello!"}'
\`\`\`

## Route Parameters

\`\`\`aayu
route "/api/posts/:id"
    get
        let post = Post.find(request.params.id)
        respond(post)
    end
    
    delete
        Post.delete(request.params.id)
        respond({"status": "deleted"})
    end
end
\`\`\`

## Full CRUD API Example

\`\`\`aayu
app TaskAPI

model Task
    id Int
    title String
    done Bool = false
end

route "/api/tasks"
    get
        respond(Task.all())
    end
    post
        Task.insert(title: request.body.title)
        respond({"status": "ok"})
    end
end

route "/api/tasks/:id"
    get
        respond(Task.find(request.params.id))
    end
    delete
        Task.delete(request.params.id)
        respond({"status": "deleted"})
    end
end

run main
\`\`\`

That's a complete REST API in **30 lines of code**! 💪`,
    exercise: "Build a REST API for a `Book` model (title, author, pages). Create GET and POST routes at `/api/books`."
  },
  {
    slug: "chapter-10",
    num: 10,
    title: "Authentication & Security",
    phase: "Database & API",
    description: "Managing user sessions, cookies, and securing routes from unauthorized access.",
    learningPoints: [
      "Why security matters for web apps",
      "Bearer token authentication",
      "Protecting routes with middleware",
      "Rate limiting to prevent abuse"
    ],
    content: `## Why Security?

Without security, anyone can:
- Read your private data
- Delete your database
- Spam your server with requests

AAYU has **built-in security features** to prevent all of this!

## Bearer Token Auth

\`\`\`aayu
app SecureAPI

model User
    id Int
    name String
    token String
end

route "/api/private"
    get
        let token = request.headers.Authorization
        if token == "Bearer my-secret-token"
            respond({"message": "Welcome, authorized user!"})
        else
            respond({"error": "Unauthorized"}, status: 401)
        end
    end
end

run main
\`\`\`

## AAYU's Built-in Security Headers

When you run with \`--web\`, AAYU automatically adds:

| Header | Purpose |
|--------|---------|
| \`X-Content-Type-Options: nosniff\` | Prevents MIME sniffing |
| \`X-Frame-Options: DENY\` | Prevents clickjacking |
| \`X-XSS-Protection: 1\` | Enables XSS filter |

## Rate Limiting

AAYU has built-in rate limiting to prevent spam:

\`\`\`aayu
app RateLimitedAPI

route "/api/data"
    get
        # AAYU automatically limits to 100 requests/minute
        respond({"data": "Here's your data"})
    end
end

run main
\`\`\`

If someone sends too many requests, they get:
\`\`\`json
{"error": "Too Many Requests"}
\`\`\`
Status code: \`429\`

## Request Size Limits

AAYU also rejects oversized requests:
\`\`\`
Max request body: 1MB (configurable)
\`\`\`

This prevents attackers from crashing your server with huge payloads.`,
    exercise: "Create a secure API where the `/api/admin` route only works if the request has a header `Authorization: Bearer admin123`. Return an error for wrong tokens."
  },
];

// Generate chapters 11-50 with titles and descriptions
const advancedChapters: Omit<ChapterData, 'content' | 'exercise'>[] = [
  { slug: "chapter-11", num: 11, title: "Declarative UI Tree", phase: "Frontend UI & UX", description: "Building interfaces natively using Page, Column, Row, and Stack widgets.", learningPoints: ["Page, Column, Row layout widgets", "Nesting widgets for complex UIs", "The widget rendering pipeline", "How AAYU converts widgets to HTML"] },
  { slug: "chapter-12", num: 12, title: "Beautiful Styling", phase: "Frontend UI & UX", description: "Colors, padding, margins, and borders. Making your app look premium out of the box.", learningPoints: ["CSS properties in AAYU widgets", "Colors, gradients, and themes", "Padding, margin, and spacing", "Responsive design basics"] },
  { slug: "chapter-13", num: 13, title: "Reactive State", phase: "Frontend UI & UX", description: "State management made easy. Watch your UI update instantly when variables change.", learningPoints: ["The 'state' keyword vs 'let'", "Automatic UI re-rendering", "State in actions and event handlers", "Reactivity under the hood"] },
  { slug: "chapter-14", num: 14, title: "Interactive Forms", phase: "Frontend UI & UX", description: "Handling user input, buttons, password fields, and binding onClick actions.", learningPoints: ["Input, TextInput, and PasswordField", "onClick and onChange handlers", "Form validation basics", "Submitting forms to routes"] },
  { slug: "chapter-15", num: 15, title: "Project: WhatsApp Clone", phase: "Frontend UI & UX", description: "Putting it all together to build a fully functional real-time chat UI.", learningPoints: ["Building a complete messaging UI", "Real-time message display", "User list and chat bubbles", "Full-stack chat application"] },
  { slug: "chapter-16", num: 16, title: "Native AI Engine", phase: "Machine Learning & AI", description: "Why AAYU doesn't need external libraries like PyTorch or Scikit-Learn.", learningPoints: ["AAYU's built-in ML engine", "No pip install needed", "How native AI differs from Python ML", "Supported algorithms"] },
  { slug: "chapter-17", num: 17, title: "K-Means Clustering", phase: "Machine Learning & AI", description: "Training your first unsupervised clustering model entirely in AAYU bytecode.", learningPoints: ["What is clustering", "K-Means algorithm explained", "Training a model in AAYU", "Visualizing cluster results"] },
  { slug: "chapter-18", num: 18, title: "Neural Networks", phase: "Machine Learning & AI", description: "Building layers, weights, biases, and activation functions from scratch natively.", learningPoints: ["Neurons, layers, and weights", "Forward propagation", "Activation functions", "Training with backpropagation"] },
  { slug: "chapter-19", num: 19, title: "RAG Systems", phase: "Machine Learning & AI", description: "Retrieval-Augmented Generation basics. Processing documents for AI context.", learningPoints: ["What is RAG", "Document chunking", "Vector search basics", "Building a Q&A system"] },
  { slug: "chapter-20", num: 20, title: "AI Data Pipelines", phase: "Machine Learning & AI", description: "Cleaning, normalizing, and streaming data directly from the AAYU database into models.", learningPoints: ["Data preprocessing", "Feature extraction", "Pipeline architecture", "DB to model data flow"] },
  { slug: "chapter-21", num: 21, title: "The Chart Widget", phase: "Graphs & Data Visualization", description: "Rendering native Line Charts, Bar Graphs, and Pie Charts directly in your AAYU UI.", learningPoints: ["Chart widget syntax", "Bar, Line, and Pie charts", "Chart.js integration", "Customizing chart appearance"] },
  { slug: "chapter-22", num: 22, title: "Real-time Data Streaming", phase: "Graphs & Data Visualization", description: "Feeding live API/Database metrics into graphs for live dashboards.", learningPoints: ["Live data updates", "SSE for real-time charts", "Database-driven dashboards", "Auto-refreshing graphs"] },
  { slug: "chapter-23", num: 23, title: "Plotting ML Predictions", phase: "Graphs & Data Visualization", description: "Visualizing K-Means clusters and Neural Network boundaries dynamically.", learningPoints: ["Scatter plots for clusters", "Decision boundary visualization", "Training progress charts", "Model accuracy plots"] },
  { slug: "chapter-24", num: 24, title: "Interactive Graphs", phase: "Graphs & Data Visualization", description: "Adding hover states, tooltips, and zoom functionality to your data plots.", learningPoints: ["Tooltip customization", "Hover and click events", "Zoom and pan controls", "Responsive chart sizing"] },
  { slug: "chapter-25", num: 25, title: "Project: Admin Dashboard", phase: "Graphs & Data Visualization", description: "Building a beautiful financial dashboard with analytics and live data charts.", learningPoints: ["Multi-chart dashboard layout", "KPI cards and metrics", "Data filtering and sorting", "Production dashboard patterns"] },
  { slug: "chapter-26", num: 26, title: "Game Loop & Ticks", phase: "Game Development", description: "Understanding the core event loop, FPS management, and delta time.", learningPoints: ["What is a game loop", "FPS and frame timing", "Delta time for smooth movement", "The tick() callback"] },
  { slug: "chapter-27", num: 27, title: "The Canvas Widget", phase: "Game Development", description: "Drawing 2D shapes, sprites, and handling pixel-perfect rendering.", learningPoints: ["Canvas widget basics", "Drawing rectangles and circles", "Colors and fill styles", "Coordinate system"] },
  { slug: "chapter-28", num: 28, title: "Physics & Collision", phase: "Game Development", description: "Implementing gravity, velocity, and AABB collision detection natively.", learningPoints: ["Gravity simulation", "Velocity and acceleration", "AABB collision detection", "Bounce and friction"] },
  { slug: "chapter-29", num: 29, title: "Keyboard & Mouse Input", phase: "Game Development", description: "Binding player movement, jumping, and shooting to real-time events.", learningPoints: ["Keyboard event binding", "Mouse click and position", "Player movement patterns", "Input debouncing"] },
  { slug: "chapter-30", num: 30, title: "Project: Flappy Bird", phase: "Game Development", description: "Building a complete, playable 2D game in a single .aayu file.", learningPoints: ["Game architecture", "Pipe generation", "Score tracking", "Game over and restart"] },
  { slug: "chapter-31", num: 31, title: "Actions & Closures", phase: "Advanced Engineering", description: "Deep dive into 'action' blocks, closures, higher-order functions, and callback patterns.", learningPoints: ["Closures and scope", "Higher-order functions", "Callback patterns", "Action as first-class values"] },
  { slug: "chapter-32", num: 32, title: "Error Handling & Exceptions", phase: "Advanced Engineering", description: "Using try/catch/throw blocks, custom error types, and graceful failure recovery.", learningPoints: ["try/catch/throw syntax", "Custom error types", "Error propagation", "Graceful degradation"] },
  { slug: "chapter-33", num: 33, title: "Async & Concurrency", phase: "Advanced Engineering", description: "Understanding AAYU's async runtime, parallel task execution, and non-blocking I/O.", learningPoints: ["Async action syntax", "Parallel task execution", "Non-blocking I/O", "Event loop internals"] },
  { slug: "chapter-34", num: 34, title: "WebSocket Magic", phase: "Advanced Engineering", description: "Building real-time bi-directional communication channels for live apps.", learningPoints: ["WebSocket basics", "Real-time messaging", "Live notifications", "Chat room implementation"] },
  { slug: "chapter-35", num: 35, title: "File I/O & Streams", phase: "Advanced Engineering", description: "Reading, writing, and streaming files. CSV parsing, JSON import/export.", learningPoints: ["Reading and writing files", "CSV parsing", "JSON import/export", "Stream processing"] },
  { slug: "chapter-36", num: 36, title: "The Package System", phase: "Package Ecosystem", description: "Understanding AAYU's official package registry, importing, and versioning.", learningPoints: ["Package registry overview", "Installing packages", "Version management", "Dependency resolution"] },
  { slug: "chapter-37", num: 37, title: "Building Your Own Package", phase: "Package Ecosystem", description: "Creating, structuring, signing, and publishing reusable AAYU packages.", learningPoints: ["Package structure", "Package manifest", "Code signing", "Publishing to registry"] },
  { slug: "chapter-38", num: 38, title: "Foreign Library Bridges", phase: "Package Ecosystem", description: "Calling C, Rust, Python, and JavaScript libraries from AAYU code.", learningPoints: ["FFI basics", "C bridge", "Rust interop", "Python/JS calling"] },
  { slug: "chapter-39", num: 39, title: "The AAYU LSP", phase: "Package Ecosystem", description: "How the Language Server Protocol powers VS Code autocomplete and diagnostics.", learningPoints: ["LSP architecture", "Autocomplete engine", "Error diagnostics", "Go-to-definition"] },
  { slug: "chapter-40", num: 40, title: "Project: Full-Stack Social App", phase: "Package Ecosystem", description: "Building a complete Instagram-like social media platform.", learningPoints: ["User authentication system", "Image upload and storage", "Feed algorithm", "Like and comment system"] },
  { slug: "chapter-41", num: 41, title: "Docker & Containers", phase: "DevOps & Deployment", description: "Containerizing your AAYU application for cloud deployment.", learningPoints: ["Dockerfile for AAYU", "Container best practices", "Multi-stage builds", "Docker Compose setup"] },
  { slug: "chapter-42", num: 42, title: "CI/CD Pipelines", phase: "DevOps & Deployment", description: "Setting up GitHub Actions for automated testing and deployment.", learningPoints: ["GitHub Actions workflow", "Automated test running", "Build and deploy pipeline", "Status badges and notifications"] },
  { slug: "chapter-43", num: 43, title: "Cloud Deployment", phase: "DevOps & Deployment", description: "Deploying to Vercel, Railway, and AWS with one command.", learningPoints: ["Vercel deployment", "Railway setup", "AWS basics", "Environment variables"] },
  { slug: "chapter-44", num: 44, title: "Monitoring & Logging", phase: "DevOps & Deployment", description: "Built-in telemetry, structured logging, and performance monitoring.", learningPoints: ["Structured logging", "Performance metrics", "Error tracking", "Health check endpoints"] },
  { slug: "chapter-45", num: 45, title: "Project: Production API", phase: "DevOps & Deployment", description: "Building and deploying a production-grade REST API with auth, rate limiting, and monitoring.", learningPoints: ["Production architecture", "Load testing", "Security hardening", "Deployment checklist"] },
  { slug: "chapter-46", num: 46, title: "Compiler Internals", phase: "Mastery & Beyond", description: "Understanding AAYU's 7-stage compiler: Lexer→Parser→AST→HIR→MIR→LIR→Bytecode.", learningPoints: ["Lexer tokenization", "Parser and AST", "IR pipeline stages", "Optimization passes"] },
  { slug: "chapter-47", num: 47, title: "VM & Bytecode Deep Dive", phase: "Mastery & Beyond", description: "How the stack-based virtual machine executes instructions, GC internals.", learningPoints: ["Stack machine architecture", "Opcode encoding", "Garbage collector", "Memory management"] },
  { slug: "chapter-48", num: 48, title: "Custom Opcodes & Extensions", phase: "Mastery & Beyond", description: "Extending the AAYU VM with your own custom bytecode instructions.", learningPoints: ["Opcode design", "VM extension API", "Custom instruction handlers", "Performance tuning"] },
  { slug: "chapter-49", num: 49, title: "Contributing to AAYU", phase: "Mastery & Beyond", description: "How to contribute to the open-source AAYU compiler and runtime.", learningPoints: ["Project structure guide", "PR and code review process", "Testing standards", "Community guidelines"] },
  { slug: "chapter-50", num: 50, title: "The Future of Intent Computing", phase: "Mastery & Beyond", description: "Ayush's vision for AAYU, the roadmap, and where intent-to-silicon goes next.", learningPoints: ["AAYU roadmap", "Intent computing vision", "Community growth", "What's next for AAYU"] },
];

// Add placeholder content for chapters 11-50
for (const ch of advancedChapters) {
  chapters.push({
    ...ch,
    content: `## ${ch.title}\n\n> 📝 Full tutorial content for this chapter is being written by Ayush Ghrit Kaushik.\n\n### What you'll learn:\n${ch.learningPoints.map(p => `- ${p}`).join('\n')}\n\n### Coming Soon\nDetailed explanations, code examples, and hands-on exercises will be added in upcoming updates. Stay tuned! 🚀`,
    exercise: `Practice what you've learned about ${ch.title.toLowerCase()}. Try writing a small AAYU program that uses the concepts from this chapter.`
  });
}
