import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';
import * as path from 'path';

let client: LanguageClient;

/**
 * AAYU VS Code Extension Entry Point
 * ----------------------------------
 * This file is executed when the extension is activated in VS Code.
 * It spawns the Python-based AAYU Language Server (LSP) as a child process
 * and establishes the JSON-RPC communication bridge between the editor and the compiler.
 */
export function activate(context: vscode.ExtensionContext) {
    console.log('AAYU Language Extension is now active!');

    // The server is implemented in Python
    const serverPath = context.asAbsolutePath(path.join('..', 'lsp', 'server.py'));
    
    // Server options to run the python script
    const serverOptions: ServerOptions = {
        command: 'python',
        args: [serverPath],
    };

    // Client options to control the language client
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.aayu')
        }
    };

    // Create the language client and start the client.
    client = new LanguageClient(
        'aayuLanguageServer',
        'AAYU Language Server',
        serverOptions,
        clientOptions
    );

    // Register BrainOS Commands
    context.subscriptions.push(
        vscode.commands.registerCommand('aayu.explain', async () => {
            const editor = vscode.window.activeTextEditor;
            const text = editor ? editor.document.getText(editor.selection) : "";
            const result = await client.sendRequest('workspace/executeCommand', {
                command: 'aayu.explain',
                arguments: [text]
            });
            vscode.window.showInformationMessage(String(result));
        }),
        vscode.commands.registerCommand('aayu.optimize', async () => {
            const editor = vscode.window.activeTextEditor;
            const text = editor ? editor.document.getText(editor.selection) : "";
            const result = await client.sendRequest('workspace/executeCommand', {
                command: 'aayu.optimize',
                arguments: [text]
            });
            vscode.window.showInformationMessage(String(result));
        }),
        vscode.commands.registerCommand('aayu.generate', async () => {
            const prompt = await vscode.window.showInputBox({ prompt: 'Describe the project to generate' });
            if (prompt) {
                const result = await client.sendRequest('workspace/executeCommand', {
                    command: 'aayu.generate',
                    arguments: [prompt]
                });
                vscode.window.showInformationMessage(String(result));
            }
        }),
        vscode.commands.registerCommand('aayu.review', async () => {
            const editor = vscode.window.activeTextEditor;
            const text = editor ? editor.document.getText() : "";
            const result = await client.sendRequest('workspace/executeCommand', {
                command: 'aayu.review',
                arguments: [text]
            });
            vscode.window.showInformationMessage(String(result));
        })
    );

    // Start the client. This will also launch the server
    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
