# Hello World

Let's build your first web server in AAYU.

## Step 1: Create a Project

If you haven't already, use the AAYU CLI to scaffold a new project:

```bash
aayu new hello-app
cd hello-app
```

This generates a standard project structure with a `main.aayu` file.

## Step 2: Write the Code

Open `main.aayu` in your favorite editor (we recommend VS Code with the AAYU extension for syntax highlighting).

```aayu
# Start the server on port 8080
serve on 8080.

# Define a GET route
get "/" to home.
    render text "Hello World from AAYU!".
end.
```

## Step 3: Run the App

From your terminal, run:

```bash
aayu run
```

AAYU will compile your code and start the Virtual Machine.
Open your browser and navigate to `http://localhost:8080`.

**Congratulations! You've just written your first AAYU web application.**

## What just happened?

1. `serve on 8080.` instructed the VM to start a multi-threaded web server.
2. `get "/" to home.` defined a route handler mapped to the root URL.
3. `render text` sent a plain-text HTTP response back to the browser.
