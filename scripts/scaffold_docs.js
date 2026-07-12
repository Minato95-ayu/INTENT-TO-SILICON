import fs from 'fs';
import path from 'path';

const packages = ['fs', 'json', 'math', 'datetime', 'crypto'];

for (const pkg of packages) {
  const content = `# aayu-${pkg}

The official AAYU standard library package for ${pkg} operations.

## Installation

\`\`\`bash
aayu install ${pkg}
\`\`\`

## Usage

\`\`\`aayu
use ${pkg}

// Example usage
// ${pkg} operations
\`\`\`
`;
  fs.writeFileSync(path.join('website', 'docs', 'packages', `${pkg}.md`), content);
}
console.log('Created markdown files for new packages.');
