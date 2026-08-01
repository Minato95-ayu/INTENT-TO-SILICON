with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    pipeline_content = f.read()

pipeline_content = pipeline_content.replace('MIRInstruction("INIT_TEXT", [])', 'MIRInstruction("INIT_TEXT", ["__DYNAMIC__"])')

with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(pipeline_content)

with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    encoder_content = f.read()

old_encoder = '''        elif isinstance(props, str):
            text_idx = self.pool.add(props)
            self._emit(Opcode.PUSH_CONST, text_idx)'''

new_encoder = '''        elif isinstance(props, str):
            if props == "__DYNAMIC__":
                pass # Skip pushing, value is already on stack
            else:
                text_idx = self.pool.add(props)
                self._emit(Opcode.PUSH_CONST, text_idx)'''

encoder_content = encoder_content.replace(old_encoder, new_encoder)

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(encoder_content)
