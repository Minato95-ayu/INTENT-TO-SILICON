import os

docs_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\docs"

docs = {
    "language_basics.md": """# AAYU Language Basics

AAYU is designed to be simple, declarative, and focused on intent.

## Variables and State

AAYU does not have `let`, `const`, or `var`. Everything that drives the UI is called `state`.

```aayu
state count = 0
state name = "Alice"
```

When state changes, any widget using that state automatically updates. No `setState` or hooks required.

## Actions

Logic in AAYU lives in `action` blocks. Actions can mutate state or perform operations.

```aayu
action increment()
    count = count + 1
end
```

## Pages

Every AAYU app is made up of Pages. A Page is a complete screen.

```aayu
page Home
    title "My App"
    text count
    button "Click Me" onClick="increment"
end
```

## The `run` keyword

The `run` keyword tells the AAYU VM to start executing the application. It should be placed at the end of your `main.aayu` file.
""",

    "widgets/text.md": """# Text Widget

Displays a string of text or a state variable on the screen.

## Syntax

```aayu
text "Hello World"
text user_name
```

## Examples

```aayu
page Profile
    text "User Profile"
    text username
end
```
""",

    "widgets/button.md": """# Button Widget

A clickable button that triggers an action.

## Syntax

```aayu
button "Submit" onClick="submitAction"
```

## Examples

```aayu
state clicked = 0

action tap()
    clicked = clicked + 1
end

page Home
    button "Click Me" onClick="tap"
end
```
""",

    "widgets/container.md": """# Container Widget

A block-level layout element used to group other widgets together.

## Syntax

```aayu
container
    text "Inside container"
end
```
""",

    "widgets/row_column.md": """# Row and Column Widgets

Used for flexing and laying out widgets horizontally (Row) or vertically (Column).

## Syntax

```aayu
row
    text "Left"
    text "Right"
end

column
    text "Top"
    text "Bottom"
end
```
""",

    "widgets/input.md": """# Input Widget

A text field for user input. Binds directly to a state variable.

## Syntax

```aayu
input "Placeholder text..." bind="state_variable"
```

## Examples

```aayu
state username = ""

page Login
    input "Enter your username" bind="username"
    text username
end
```
""",

    "migration/react.md": """# React to AAYU

If you are coming from React, AAYU will feel incredibly refreshing.

## No Hooks

In React:
```jsx
const [count, setCount] = useState(0);
const increment = () => setCount(count + 1);
```

In AAYU:
```aayu
state count = 0
action increment()
    count = count + 1
end
```

## No Fragments or Return Statements

AAYU's tree is declarative by default. You don't need `return ( <> ... </> )`. Just declare widgets inside a `page` or `container`.
""",

    "migration/flutter.md": """# Flutter to AAYU

AAYU abstracts away the widget tree boilerplate.

## Less Nesting

In Flutter:
```dart
return Scaffold(
  appBar: AppBar(title: Text("Home")),
  body: Column(
    children: [
      Text("Hello"),
    ]
  )
);
```

In AAYU:
```aayu
page Home
    title "Home"
    column
        text "Hello"
    end
end
```
""",
    
    "learn/lesson_1.md": """# Lesson 1: Hello World

Welcome to AAYU! Let's build your first app in 1 minute.

Every AAYU app starts with an `app` declaration and ends with `run`.

```aayu
app hello_world

page Home
    text "Hello World!"
end

run
```

**Try it yourself:** Run `aayu new my_app`, open `main.aayu`, paste the code above, and run `aayu run`.
""",

    "learn/lesson_2.md": """# Lesson 2: Pages and Titles

An app can have multiple pages. Each page represents a full screen. You can set the title of a page using the `title` widget.

```aayu
app title_app

page Home
    title "My Amazing App"
    text "This is the content."
end

run
```
""",

    "learn/lesson_3.md": """# Lesson 3: State

State holds your application's data. To define state, use the `state` keyword.

```aayu
app state_app

state username = "Alice"

page Home
    text "Welcome back,"
    text username
end

run
```
""",

    "learn/lesson_4.md": """# Lesson 4: Actions and Buttons

To make your app interactive, you need `action` blocks. Actions can modify state. You trigger actions using buttons.

```aayu
app counter

state count = 0

action click()
    count = count + 1
end

page Home
    text count
    button "Increment" onClick="click"
end

run
```
""",

    "learn/lesson_5.md": """# Lesson 5: Layouts

Use `row` and `column` to position your widgets.

```aayu
app layout_app

page Home
    row
        text "Left"
        text "Right"
    end
    
    column
        button "Top"
        button "Bottom"
    end
end

run
```
"""
}

# Create directories
os.makedirs(os.path.join(docs_dir, "widgets"), exist_ok=True)
os.makedirs(os.path.join(docs_dir, "migration"), exist_ok=True)
os.makedirs(os.path.join(docs_dir, "learn"), exist_ok=True)

# Write files
for path, content in docs.items():
    full_path = os.path.join(docs_dir, path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Docs generated successfully!")
