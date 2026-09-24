import os

with open("src/self_hosted/lexer.aayu", "r", encoding="utf-8") as f:
    lexer_code = f.read()

# We will remove the current driver code at the bottom of lexer.aayu, which looks like:
# let source_code = "..."
driver_idx = lexer_code.find('let source_code =')
if driver_idx != -1:
    lexer_code = lexer_code[:driver_idx]

# Append new clean driver
driver = """
action main()
    let src = "let x = 10"
    print("Lexing Native Code:")
    print(src)
    
    let tokens = tokenize(src)
    let length = len(tokens)
    
    print("Tokens found:")
    print(length)
    
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

with open("test_lexer_native.aayu", "w", encoding="utf-8") as f:
    f.write(lexer_code + driver)
