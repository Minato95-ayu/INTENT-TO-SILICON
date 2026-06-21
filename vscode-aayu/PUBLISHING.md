# Publishing AAYU to the VS Code Marketplace

Follow these steps to publish the already built `aayu-1.0.0.vsix` extension to the VS Code Marketplace.

## 1. Prerequisites
Ensure you have Node.js and the `vsce` CLI installed globally:
```bash
npm install -g @vscode/vsce
```

## 2. Create a Publisher Account
1. Go to the [Visual Studio Marketplace Management Page](https://marketplace.visualstudio.com/manage).
2. Login with your Microsoft account.
3. Click **Create Publisher** and use `aayu-lang` or your chosen publisher name.

## 3. Generate a Personal Access Token (PAT)
1. Go to [Azure DevOps](https://dev.azure.com/).
2. Login and navigate to your **User settings** (top right) -> **Personal Access Tokens**.
3. Click **New Token**.
4. Give it a name (e.g. `VSCE Publish`).
5. Set **Organization** to `All accessible organizations`.
6. Set **Scopes** to `Custom defined`.
7. Click **Show all scopes** at the bottom.
8. Scroll down to **Marketplace** and select **Acquire** and **Manage**.
9. Click **Create** and **Copy** the token.

## 4. Publish the Extension
Open your terminal in the `vscode-aayu` directory and run:

```bash
# Login using the publisher name and the PAT you just generated
vsce login aayu-lang

# Publish the extension
vsce publish
```

Alternatively, you can just drag and drop the `aayu-1.0.0.vsix` file into the [Manage Extensions Page](https://marketplace.visualstudio.com/manage) in your browser!
