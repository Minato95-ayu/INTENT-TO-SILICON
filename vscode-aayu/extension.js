const path = require('path');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');
const { workspace } = require('vscode');

let client;

function getPythonPath() {
    // Basic detection for OS
    const platform = process.platform;
    if (platform === 'win32') {
        return 'python'; // 'py' or 'python' works on most Windows
    }
    return 'python3';
}

function activate(context) {
    const pythonPath = getPythonPath();
    // Path to the AAYU Language Server
    const serverModule = context.asAbsolutePath(
        path.join('..', 'prototype', 'aayu_language', 'aayu_lsp.py')
    );

    const serverOptions = {
        run: { 
            command: pythonPath, 
            args: [serverModule], 
            transport: TransportKind.stdio 
        },
        debug: { 
            command: pythonPath, 
            args: [serverModule], 
            transport: TransportKind.stdio 
        }
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/*.aayu')
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

function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

module.exports = {
    activate,
    deactivate
};
