with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''        if isinstance(props, dict):
            # For widgets with text content, push the text
            text = props.get("text", props.get("title", props.get("name", "")))
            if text:
                text_idx = self.pool.add(str(text))
                self._emit(Opcode.PUSH_CONST, text_idx)
            else:
                # Push empty string for widgets without text content
                empty_idx = self.pool.add("")
                self._emit(Opcode.PUSH_CONST, empty_idx)'''

new_code = '''        if isinstance(props, dict):
            # For text fallback in older tests, we should probably keep 'value' mapping
            if "text" in props and "value" not in props:
                props["value"] = props["text"]
            elif "title" in props and "value" not in props:
                props["value"] = props["title"]
            elif "name" in props and "value" not in props:
                props["value"] = props["name"]
            
            idx = self.pool.add(props)
            self._emit(Opcode.PUSH_CONST, idx)'''

content = content.replace(old_code, new_code)

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(content)
