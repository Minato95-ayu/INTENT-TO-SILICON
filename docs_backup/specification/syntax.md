# Syntax Basics

AAYU is designed to be highly readable, favoring English-like keywords over excessive punctuation. 

## Statements and Termination

All statements and declarative blocks in AAYU must end with a period (`.`).

```aayu
number max_users is 100.
show max_users.
```

## Blocks

Blocks of code, such as `task` definitions, `entity` bodies, or `if` statements, begin with a declaration and are closed with the `end.` keyword.

```aayu
task greet with name.
    show "Hello, " + name.
end.
```

## Variables and Assignment

Variables in AAYU are strongly typed. They are declared using their type, followed by the identifier, the `is` keyword, and the initial value.

```aayu
text message is "Welcome to AAYU".
number count is 42.
boolean is_active is true.
```

Reassignment is done using the `is` keyword without the type declaration (if the variable already exists in scope), or by updating map properties.

## Comments

Comments begin with the `#` symbol and extend to the end of the line.

```aayu
# This is a comment
number age is 30. # This is an inline comment
```

## Operators

AAYU supports standard operators, often utilizing English words for boolean logic to maintain readability.

### Arithmetic
- `+` (Addition, String Concatenation)
- `-` (Subtraction)
- `*` (Multiplication)
- `/` (Division)

### Comparison
- `equal to` (==)
- `not_equal to` (!=)
- `<` (Less than)
- `>` (Greater than)

### Logical
- `and` (Logical AND)
- `or` (Logical OR)
- `not` (Logical NOT)

## Control Flow

### If / Else Statements

```aayu
number score is 85.

if score > 80.
    show "Excellent".
else.
    show "Good".
end.
```

### Loops

AAYU supports `while` loops and `foreach` loops for iterating over lists.

**While Loop:**
```aayu
number i is 0.
while i < 5.
    show i.
    number i is i + 1.
end.
```

**Foreach Loop:**
```aayu
list names is ["Alice", "Bob", "Charlie"].
foreach name in names.
    show name.
end.
```
