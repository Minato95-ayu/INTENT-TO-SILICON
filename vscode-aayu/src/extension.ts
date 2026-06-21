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
  // Path to the Python executable (can be configured or default to 'python')
  const pythonPath = workspace.getConfiguration('aayu').get<string>('pythonPath', 'python');
  
  // Path to the LSP server script relative to the extension or absolute
  // During development, it's at prototype/aayu_language/lsp_server.py
  // Assuming the workspace root contains INTENT-TO-SILICON
  
  const serverPath = context.asAbsolutePath(path.join('..', 'prototype', 'aayu_language', 'lsp_server.py'));

  const run: Executable = {
    command: pythonPath,
    args: [serverPath]
  };

  const serverOptions: ServerOptions = {
    run: run,
    debug: run
  };

  const clientOptions: LanguageClientOptions = {
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

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
