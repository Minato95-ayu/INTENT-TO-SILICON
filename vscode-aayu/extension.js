const { spawn } = require('node:child_process');
const path = require('node:path');
const vscode = require('vscode');

function activate(context) {
    const output = vscode.window.createOutputChannel('AAYU');
    context.subscriptions.push(output);
    context.subscriptions.push(vscode.commands.registerCommand('aayu.runFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'aayu' || !editor.document.fileName.endsWith('.aayu')) {
            vscode.window.showErrorMessage('Open an AAYU .aayu source file before running it.');
            return;
        }

        const config = vscode.workspace.getConfiguration('aayu');
        const executable = config.get('executablePath', 'aayu-vm');
        const compilerPath = config.get('compilerPath', '');
        const cwd = vscode.workspace.getWorkspaceFolder(editor.document.uri)?.uri.fsPath
            ?? path.dirname(editor.document.fileName);
        const env = { ...process.env };
        if (compilerPath) env.AAYU_COMPILER_PATH = compilerPath;

        output.clear();
        output.show(true);
        output.appendLine(`> ${executable} run ${editor.document.fileName}`);
        const child = spawn(executable, ['run', editor.document.fileName], { cwd, env, windowsHide: true });
        child.stdout.on('data', data => output.append(data.toString()));
        child.stderr.on('data', data => output.append(data.toString()));
        child.on('error', error => {
            output.appendLine(`Failed to start AAYU VM: ${error.message}`);
            vscode.window.showErrorMessage(`Could not start AAYU VM: ${error.message}`);
        });
        child.on('close', code => output.appendLine(`\nProcess exited with code ${code ?? 'unknown'}.`));
    }));
}

function deactivate() {}

module.exports = { activate, deactivate };
