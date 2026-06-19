"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const path = require("path");
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
let client;
function activate(context) {
    // The server is implemented in Python
    // Assuming the python script is one level above the extension root in the `aayu_language` folder.
    // For local prototype:
    const serverModule = path.join(context.extensionPath, '..', 'aayu_language', 'aayu_lsp.py');
    // Command to run
    const run = {
        command: 'python',
        args: [serverModule]
    };
    // If the extension is launched in debug mode then the debug server options are used
    // Otherwise the run options are used
    const serverOptions = {
        run: run,
        debug: run
    };
    // Options to control the language client
    const clientOptions = {
        // Register the server for aayu documents
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            // Notify the server about file changes to '.aayu files contained in the workspace
            fileEvents: vscode_1.workspace.createFileSystemWatcher('**/.aayu')
        }
    };
    // Create the language client and start the client.
    client = new node_1.LanguageClient('aayuLanguageServer', 'Aayu Language Server', serverOptions, clientOptions);
    // Start the client. This will also launch the server
    client.start();
}
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
//# sourceMappingURL=extension.js.map