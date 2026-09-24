import os

with open("src/self_hosted/lexer.aayu", "r", encoding="utf-8") as f:
    lexer_code = f.read()

with open("src/self_hosted/parser.aayu", "r", encoding="utf-8") as f:
    parser_code = f.read()

# Strip lexer driver
l_driver = lexer_code.find('let source_code =')
if l_driver != -1:
    lexer_code = lexer_code[:l_driver]

# Strip parser driver
p_driver = parser_code.find('let parser_src =')
if p_driver != -1:
    parser_code = parser_code[:p_driver]

driver = """
action print_ast(ast)
    let length = len(ast["statements"])
    print("Program Statements:")
    print(length)
    
    let i = 0
    while i < length
        let stmt = ast["statements"][i]
        print(stmt["type"])
        i = i + 1
    end
    return 0
end

action main()
    let src = "let x = 10 \n let y = 20 \n print(x + y)"
    print("Parsing Native Code:")
    print(src)
    
    let tokens = tokenize(src)
    let ast = parse(tokens)
    print_ast(ast)
end

main()
"""

with open("test_parser_native.aayu", "w", encoding="utf-8") as f:
    f.write(lexer_code + "\n" + parser_code + "\n" + driver)
