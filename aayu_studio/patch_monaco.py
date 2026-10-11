import os

file_path = 'D:/Topptic/app/components/editor/EditorPanel.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I want to inject AAYU syntax. We can use the monaco.languages.register API inside a hook, or in beforeMount.
# Let's find where MonacoEditor is rendered or if there's a beforeMount prop.

aayu_syntax = '''
function handleEditorWillMount(monaco: any) {
  monaco.languages.register({ id: 'aayu' });
  monaco.languages.setMonarchTokensProvider('aayu', {
    keywords: ['app', 'model', 'route', 'action', 'run', 'end', 'let', 'state', 'get', 'post', 'put', 'delete', 'Page', 'Column', 'Text', 'Button', 'Row', 'TextField'],
    typeKeywords: ['Int', 'String', 'Float', 'Bool', 'Tensor'],
    operators: ['=', '>', '<', '==', '<=', '>=', '!=', '+', '-', '*', '/'],
    symbols:  /[=><!~?:&|+\-*\/\^%]+/,
    tokenizer: {
      root: [
        [/[a-zA-Z_]\w*/, { cases: { '@typeKeywords': 'type', '@keywords': 'keyword', '@default': 'identifier' } }],
        [/[{}()\[\]]/, '@brackets'],
        [/@symbols/, { cases: { '@operators': 'operator', '@default': '' } }],
        [/\d*\.\d+([eE][\-+]?\d+)?/, 'number.float'],
        [/\d+/, 'number'],
        [/"([^"\\]|\\.)*$/, 'string.invalid'],
        [/"/, { token: 'string.quote', bracket: '@open', next: '@string' }],
        [/\/\/.*$/, 'comment'],
      ],
      string: [
        [/[^\\"]+/, 'string'],
        [/\\./, 'string.escape.invalid'],
        [/"/, { token: 'string.quote', bracket: '@close', next: '@pop' }]
      ],
    }
  });
}
'''

if 'handleEditorWillMount' not in content:
    # Inject it before the component export
    content = content.replace('export function EditorPanel(', aayu_syntax + '\nexport function EditorPanel(')
    
    # Add beforeMount={handleEditorWillMount} to MonacoEditor
    content = content.replace('<MonacoEditor', '<MonacoEditor\n        beforeMount={handleEditorWillMount}')
    
    # Also we should change the default code in app/lib/constants.ts
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

with open('D:/Topptic/app/lib/constants.ts', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('export const DEFAULT_EDITOR_CODE = ', 'export const DEFAULT_EDITOR_CODE = pp Hello\\n\\naction main\\n    print("Welcome to AAYU Studio!")\\nend\\n\\nrun main;//')
with open('D:/Topptic/app/lib/constants.ts', 'w', encoding='utf-8') as f:
    f.write(c)

