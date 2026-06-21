# Hello World

Writing code in AAYU is just like writing a natural sentence.

## Your First Program

Create a file named `hello.aayu` and add the following code:

```aayu
show "Hello World!".
```

Now, run it from your terminal:
```bash
aayu run hello.aayu
```

### Variables and Logic

Variables are declared simply using the `set` keyword, and compared using natural `if` statements.

```aayu
set "age" to 20.

if age > 18 then.
    show "You are an adult.".
else.
    show "You are a minor.".
end.
```

### Functions (Tasks)

In AAYU, functions are called `tasks`.

```aayu
task greet with name.
    show "Hello, " + name.
end.

greet("Developer").
```

That's it! You've learned the core basics of AAYU. Now, let's look at building something real, like a [Web Server](/examples/todo-app).
