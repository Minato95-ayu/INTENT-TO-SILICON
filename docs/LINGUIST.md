# Getting AAYU Recognized by GitHub Linguist

To get `.aayu` syntax highlighting natively on GitHub, we need to submit a Pull Request to the [github/linguist](https://github.com/github/linguist) repository.

## 1. Fork and Clone
Fork the `github/linguist` repository to your GitHub account and clone it locally.

## 2. Update `languages.yml`
Open `lib/linguist/languages.yml` in the linguist repo, and add the AAYU configuration alphabetically:

```yaml
AAYU:
  type: programming
  color: "#6E56CF"
  extensions:
  - ".aayu"
  tm_scope: source.aayu
  ace_mode: text
  language_id: 123456 # (Replace with a random unused 6-digit ID)
```

## 3. Add the TextMate Grammar
Linguist needs the TextMate grammar to know how to highlight the code.
Since Linguist relies on external submodules for grammars, the standard practice is:
1. Push your `vscode-aayu` repository to GitHub as a public repo.
2. In the `linguist` repo, run the script to add your repo as a submodule for the grammar.
```bash
script/add-grammar https://github.com/aayu-lang/vscode-aayu
```

## 4. Add Snippets
Add a couple of small sample files inside the `samples/AAYU/` directory in the linguist repo.
Example `samples/AAYU/hello.aayu`:
```aayu
task main.
    show "Hello World".
end.
```

## 5. Submit the PR
Commit your changes and submit a Pull Request to `github/linguist`. Include context that AAYU is a new human-readable intent-based language. Once merged, all `.aayu` files on GitHub will have syntax highlighting and be categorized as AAYU language!
