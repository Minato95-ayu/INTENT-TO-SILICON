# Getting AAYU Recognized by GitHub Linguist

To get `.aayu` syntax highlighting natively on GitHub, we need to submit a Pull Request to the [github/linguist](https://github.com/github/linguist) repository.

## 1. Add repository-level language attribution

Add a root `.gitattributes` file to force `.aayu` files to be recognized as AAYU in GitHub language statistics:

```gitattributes
*.aayu linguist-language=Aayu
```

This helps the repo show AAYU as the main language even before the official Linguist merge.

## 2. Fork and Clone Linguist

Fork the `github/linguist` repository to your GitHub account and clone it locally.

```bash
git clone https://github.com/<your-username>/linguist.git
cd linguist
```

## 3. Update `languages.yml`

Open `lib/linguist/languages.yml` in the linguist repo, and add the AAYU configuration alphabetically:

```yaml
- name: AAYU
  type: programming
  color: "#cc0000"
  aliases:
    - aayu
  extensions:
    - .aayu
  filenames: []
  interpreters:
    - aayu
  ace_mode: text
  codemirror_mode: null
  codemirror_mime_type: null
  tm_scope: source.aayu
  wrap: false
  escape_char: '\\'
  searchable: true
```

## 4. Add grammar samples

In the `linguist` repo, add a few sample files under `samples/AAYU/`.

Example `samples/AAYU/hello.aayu`:

```aayu
task main.
    show "Hello World".
end.
```

Add a second sample that demonstrates pages, entities, and workflows.

## 5. Add the TextMate grammar reference

Link the grammar source to the AAYU VS Code extension repo. Use the Linguist grammar tooling or include a note in the PR description explaining that the grammar lives in the `vscode-aayu` repository.

## 6. Submit the PR

Commit your changes and open a Pull Request against `github/linguist`.

- Explain that AAYU is a new intent-first programming language
- Include `.aayu` samples
- Reference the VS Code package and TextMate grammar
- Mention the repo: `https://github.com/Minato95-ayu/INTENT-TO-SILICON`

After merge, GitHub will classify `.aayu` files as AAYU and the repo language bar will show AAYU as the primary language.
