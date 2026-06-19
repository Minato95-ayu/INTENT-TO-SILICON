import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions
} from 'vscode-languageclient/node';
import * as os from 'os';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    console.log('AAYU extension is now active!');

    // Command to start the LSP server. 
    // In production, `aayu` must be in the system PATH.
    // For now, if we are in Windows, it might be aayu.cmd, but `aayu` will resolve.
    // However, since we're just testing locally, we can just run the global `aayu lsp`
    let command = 'aayu';
    
    // We assume the user has aliased `aayu` globally or we can fallback to python execution.
    // Actually, to make it foolproof for our demo, let's allow it to spawn from python directly if needed.
    // But since the user installed AAYU CLI in their system path (or aliased it), `aayu lsp` should work.
    
    let serverOptions: ServerOptions = {
        run: { command: command, args: ['lsp'] },
        debug: { command: command, args: ['lsp'] }
    };

    let clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.clientrc')
        }
    };

    client = new LanguageClient(
        'aayuLanguageServer',
        'AAYU Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
