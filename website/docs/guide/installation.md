# Installation

AAYU is designed to be installed in seconds. You don't need to manually configure PATH variables or install complex toolchains.

## Windows

Open PowerShell and run the following command:

```powershell
# Coming soon: The official aayu Windows installer
# aayu install
```

## Linux / macOS

Open your terminal and run the following command:

```bash
curl -fsSL https://aayu.org/install.sh | bash
```

## Verify Installation

Once installed, verify that the `aayu` command is available:

```bash
aayu --version
```

You should see output similar to:
```text
AAYU Compiler v0.1.0 (Python VM Edition)
```

## Creating Your First Project

Now that AAYU is installed, you can generate a new project in one command:

```bash
aayu new my-first-app
```

This will create a folder called `my-first-app` with a ready-to-run web server.

[Go to Hello World &rarr;](/guide/hello-world)
