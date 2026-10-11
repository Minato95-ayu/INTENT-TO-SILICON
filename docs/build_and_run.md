# Build and Run

AAYU makes it incredibly simple to test and compile your application for multiple targets.

## Running Locally

To run your application in development mode with the VM:

```bash
aayu run
```
*This will execute `main.aayu` in the current directory.*

## Building for Desktop

AAYU uses PyInstaller to bundle your AAYU bytecode and VM into a single native executable.

```bash
aayu build
```
*(Defaults to your host OS, e.g., Windows `.exe`)*

The output will be placed in `build/release/app.exe`.
You can simply double-click `app.exe` to launch your program!

## Building for Web

To transpile your AAYU application into a standard HTML/JS web bundle:

```bash
aayu build --target web
```

The output will be placed in `build/web/`.
You can open `build/web/index.html` directly in your browser.