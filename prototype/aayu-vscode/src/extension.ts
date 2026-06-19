import * as path from 'path';
import { workspace, ExtensionContext } from 'vscode';

import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    Executable
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    // The server is implemented in Python
    // Assuming the python script is one level above the extension root in the `aayu_language` folder.
    // For local prototype:
    const serverModule = path.join(context.extensionPath, '..', 'aayu_language', 'aayu_lsp.py');
    
    // Command to run
    const run: Executable = { 
        command: 'python', 
        args: [serverModule]
    };

    // If the extension is launched in debug mode then the debug server options are used
    // Otherwise the run options are used
    const serverOptions: ServerOptions = {
        run: run,
        debug: run
    };

    // Options to control the language client
    const clientOptions: LanguageClientOptions = {
        // Register the server for aayu documents
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            // Notify the server about file changes to '.aayu files contained in the workspace
            fileEvents: workspace.createFileSystemWatcher('**/.aayu')
        }
    };

    // Create the language client and start the client.
    client = new LanguageClient(
        'aayuLanguageServer',
        'Aayu Language Server',
        serverOptions,
        clientOptions
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
