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
    // We launch the global 'aayu' executable with 'lsp' argument
    const command = 'aayu';
    const args = ['lsp'];

    const executable: Executable = {
        command,
        args,
        options: { env: process.env }
    };

    const serverOptions: ServerOptions = {
        run: executable,
        debug: executable
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'aayu' }],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/*.aayu')
        }
    };

    // Create the language client and start the client.
    client = new LanguageClient(
        'aayuLanguageServer',
        'AAYU Language Server',
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
