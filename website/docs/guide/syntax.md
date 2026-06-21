# Syntax Basics

AAYU is designed to be as close to natural language as possible. It eliminates the need for curly braces `{}`, semicolons `;`, and complex syntax rules. 

An AAYU block begins with a declaration (like `task`, `entity`, or `role`) and is explicitly closed using the `end.` keyword. Every statement in AAYU **must end with a period `.`**, giving it the feel of an English sentence.

## Tasks and Printing

The `task` keyword is used to define functions or entry points. The main entry point of an AAYU application is `task main.`.

```aayu
task main.
    print "Hello AAYU".
end.
```

## Variables

Variables in AAYU are strongly typed. You define them by declaring the type followed by the variable name.

```aayu
text name.
number age.
boolean is_active.
```

To assign a value, use the `set` keyword:

```aayu
set name to "John Doe".
set age to 25.
set is_active to true.
```

## Conditionals

AAYU supports natural language if-else constructs.

```aayu
if age > 18.
    print "Eligible".
else.
    print "Not Eligible".
end.
```

## Maps (Dictionaries)

Maps allow you to store key-value pairs natively.

```aayu
map user_data.
set user_data["name"] to "Alice".
set user_data["role"] to "Admin".
```

## Built-in Modules

AAYU comes with an extensive standard library. You can include them using the `use` keyword.

```aayu
use http.
use db.
use auth.
use rbac.
use workflow.
```

When you use AAYU for web development, the true power of the syntax shines. Head over to the **Web Development** section to see how entities, relations, and routes are declared.
