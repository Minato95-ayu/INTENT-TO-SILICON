const { LanguageClient, TransportKind } = require('vscode-languageclient/node');
const { workspace, window } = require('vscode');
const cp = require('child_process');

let client;

function checkAayuInstalled() {
    try {
        // Try to run 'aayu --version' to see if it's in PATH
        cp.execSync('aayu --version', { stdio: 'ignore' });
        return true;
    } catch (e) {
        return false;
    }
}

function activate(context) {
    if (!checkAayuInstalled()) {
        window.showErrorMessage('AAYU CLI not found. Run: pip install aayu-lang');
        return;
    }

    const serverOptions = {
        run: { 
            command: 'aayu', 
            args: ['lsp'], 
            transport: TransportKind.stdio 
        },
        debug: { 
            command: 'aayu', 
            args: ['lsp'], 
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
