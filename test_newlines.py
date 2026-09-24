import os
with open("src/self_hosted/lexer.aayu", "r", encoding="utf-8") as f:
    lexer_code = f.read()

l_driver = lexer_code.find('let source_code =')
if l_driver != -1: lexer_code = lexer_code[:l_driver]

driver = """
action main()
    let src = "let x = 10 \\n let y = 20 \\n print(x + y)"
    let tokens = tokenize(src)
    let length = len(tokens)
    let i = 0
    while i < length
        let t = tokens[i]
        print(t["type"])
        print(t["value"])
        i = i + 1
    end
end
main()
"""

with open("test_lexer_native_newlines.aayu", "w", encoding="utf-8") as f:
    f.write(lexer_code + "\n" + driver)
