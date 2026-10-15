const { spawn } = require('node:child_process');
const path = require('node:path');
const vscode = require('vscode');

function activate(context) {
    const output = vscode.window.createOutputChannel('AAYU');
    context.subscriptions.push(output);

    function runAayuCommand(args, description) {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'aayu' || !editor.document.fileName.endsWith('.aayu')) {
            vscode.window.showErrorMessage('Open an AAYU .aayu source file before running this command.');
            return;
        }

        const config = vscode.workspace.getConfiguration('aayu');
        const executable = config.get('executablePath', 'aayu');
        const compilerPath = config.get('compilerPath', '');
        const cwd = vscode.workspace.getWorkspaceFolder(editor.document.uri)?.uri.fsPath
            ?? path.dirname(editor.document.fileName);
        const env = { ...process.env };
        if (compilerPath) env.AAYU_COMPILER_PATH = compilerPath;

        output.clear();
        output.show(true);
        output.appendLine(`> ${executable} ${args.join(' ')}`);

        const child = spawn(executable, args, { cwd, env, windowsHide: true });
        child.stdout.on('data', data => output.append(data.toString()));
        child.stderr.on('data', data => output.append(data.toString()));
        child.on('error', error => {
            output.appendLine(`Failed to start AAYU (${description}): ${error.message}`);
            vscode.window.showErrorMessage(`Could not start AAYU: ${error.message}`);
        });
        child.on('close', code => output.appendLine(`\nProcess exited with code ${code ?? 'unknown'}.`));
    }

    // 1. Run File
    context.subscriptions.push(vscode.commands.registerCommand('aayu.runFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['run', editor.document.fileName], 'Run Current File');
    }));

    // 2. Run Test Suite
    context.subscriptions.push(vscode.commands.registerCommand('aayu.runTest', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['test', editor.document.fileName], 'Run Test Suite');
    }));

    // 2a. AI Agent Tokenizer & Context Optimizer
    context.subscriptions.push(vscode.commands.registerCommand('aayu.tokenAudit', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['token', editor.document.fileName], 'Audit BPE Tokens & Compress Context');
    }));

    // 2b. Autonomous Code Repair
    context.subscriptions.push(vscode.commands.registerCommand('aayu.repairFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['repair', editor.document.fileName], 'Auto-Heal Syntax Anomalies');
    }));

    // 2c. Architecture Graph Visualizer
    context.subscriptions.push(vscode.commands.registerCommand('aayu.graphFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['graph', editor.document.fileName], 'Visualize Architecture Graph');
    }));

    // 3. Format Document
    context.subscriptions.push(vscode.commands.registerCommand('aayu.formatFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['fmt', editor.document.fileName], 'Format Document');
    }));

    // 4. Lint Current File
    context.subscriptions.push(vscode.commands.registerCommand('aayu.lintFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['lint', editor.document.fileName], 'Lint Document');
    }));

    // 5. Cryptographic Lockfile Verification
    context.subscriptions.push(vscode.commands.registerCommand('aayu.lockFile', () => {
        runAayuCommand(['lock', '--verify'], 'Lockfile Verification');
    }));

    // 6. Microsecond Execution & Memory Profiler
    context.subscriptions.push(vscode.commands.registerCommand('aayu.profileFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['profile', editor.document.fileName], 'Profile Execution');
        else runAayuCommand(['profile'], 'Profile Execution');
    }));

    // 7. Native Fuzz Testing
    context.subscriptions.push(vscode.commands.registerCommand('aayu.fuzzFile', () => {
        runAayuCommand(['fuzz'], 'Fuzz Testing');
    }));

    // 8. Disassemble Bytecode
    context.subscriptions.push(vscode.commands.registerCommand('aayu.disasmFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) runAayuCommand(['disasm', editor.document.fileName], 'Disassemble Bytecode');
    }));

    // 5. Pack Standalone Binary
    context.subscriptions.push(vscode.commands.registerCommand('aayu.packFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const outPath = editor.document.fileName.replace(/\.aayu$/, '.ayc');
            runAayuCommand(['pack', editor.document.fileName, '-o', outPath], 'Pack Binary');
        }
    }));

    // 6. Run Benchmark
    context.subscriptions.push(vscode.commands.registerCommand('aayu.benchFile', () => {
        runAayuCommand(['bench'], 'Run Benchmark');
    }));
}

function deactivate() {}

module.exports = { activate, deactivate };
