with open('src/self_hosted/lexer.aayu', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('LexerState(source: src, pos: 0, line: 1, column: 1, length: len(src))', 'LexerState(src, 0, 1, 1, len(src))')
text = text.replace('Token(type: tok_type, value: value, line: start_line, column: start_col)', 'Token(tok_type, value, start_line, start_col)')
text = text.replace('Token(type: "NUMBER", value: value, line: start_line, column: start_col)', 'Token("NUMBER", value, start_line, start_col)')
text = text.replace('Token(type: "STRING", value: value, line: start_line, column: start_col)', 'Token("STRING", value, start_line, start_col)')
text = text.replace('Token(type: "EOF", value: "", line: st.line, column: st.column)', 'Token("EOF", "", st.line, st.column)')
text = text.replace('Token(type: "PUNCTUATION", value: val, line: st.line, column: st.column - 1)', 'Token("PUNCTUATION", val, st.line, st.column - 1)')


with open('src/self_hosted/lexer.aayu', 'w', encoding='utf-8') as f:
    f.write(text)
