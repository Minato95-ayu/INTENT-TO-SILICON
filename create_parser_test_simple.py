import os

with open("src/self_hosted/lexer.aayu", "r", encoding="utf-8") as f:
    lexer_code = f.read()
with open("src/self_hosted/parser.aayu", "r", encoding="utf-8") as f:
    parser_code = f.read()

# Strip drivers
l_driver = lexer_code.find('let source_code =')
if l_driver != -1: lexer_code = lexer_code[:l_driver]
p_driver = parser_code.find('let parser_src =')
if p_driver != -1: parser_code = parser_code[:p_driver]

driver = """
action main()
    let src = "let x = 10"
    
    let tokens = tokenize(src)
    let length = len(tokens)
    
    let i = 0
    while i < length
        let t = tokens[i]
        print(t["type"])
        print(t["value"])
        i = i + 1
    end
    
    let ast_res = parse(tokens)
    print("Parsed OK")
end

main()
"""

with open("test_parser_native_simple.aayu", "w", encoding="utf-8") as f:
    f.write(lexer_code + "\n" + parser_code + "\n" + driver)
