with open('compiler/bytecode/encoder.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_dataclass = '''class EncodedProgram:
    \"\"\"The complete encoded bytecode output.\"\"\"
    header: BinaryHeader
    bytecode: bytearray
    constant_pool: ConstantPool
    relocation_table: List[Relocation] = field(default_factory=list)'''

new_dataclass = '''class EncodedProgram:
    \"\"\"The complete encoded bytecode output.\"\"\"
    header: BinaryHeader
    bytecode: bytearray
    constant_pool: ConstantPool
    relocation_table: List[Relocation] = field(default_factory=list)
    action_addresses: dict = field(default_factory=dict)'''

content = content.replace(old_dataclass, new_dataclass)

old_return = '''        return EncodedProgram(
            header=header,
            bytecode=self.bytecode,
            constant_pool=self.pool,
            relocation_table=self.relocations
        )'''

new_return = '''        return EncodedProgram(
            header=header,
            bytecode=self.bytecode,
            constant_pool=self.pool,
            relocation_table=self.relocations,
            action_addresses=self._action_addresses
        )'''

content = content.replace(old_return, new_return)

with open('compiler/bytecode/encoder.py', 'w', encoding='utf-8') as f:
    f.write(content)
