
import os

with open("runtime/vm/interpreter.py", "r", encoding="utf-8") as f:
    code = f.read()

patch = """    def op_DB_INSERT(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        
        info = self.vm.constant_pool[idx]
        model_name = info["model"]
        fields_count = info["fields_count"]
        
        fields = {}
        for _ in range(fields_count):
            val = self.vm.value_stack.pop()
            key = self.vm.value_stack.pop()
            fields[key] = val
        
        import sqlite3
        try:
            conn = sqlite3.connect("aayu_db.sqlite")
            c = conn.cursor()
            cols = ", ".join(fields.keys())
            placeholders = ", ".join(["?"] * len(fields))
            vals = tuple(fields.values())
            c.execute(f"CREATE TABLE IF NOT EXISTS {model_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols})")
            c.execute(f"INSERT INTO {model_name} ({cols}) VALUES ({placeholders})", vals)
            conn.commit()
            conn.close()
            print(f"[VM-DB] Successfully inserted into {model_name}: {fields}")
        except Exception as e:
            print(f"[VM-DB-ERROR] Insert failed: {e}")
        return True

    def op_DB_FIND(self, opcode):
        idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
        self.vm.registers.ip += 3
        model_name = self.vm.constant_pool[idx]
        
        import sqlite3
        try:
            conn = sqlite3.connect("aayu_db.sqlite")
            c = conn.cursor()
            c.execute(f"SELECT * FROM {model_name}")
            rows = c.fetchall()
            conn.close()
            self.vm.value_stack.push(rows)
            print(f"[VM-DB] Found {len(rows)} records in {model_name}")
        except Exception as e:
            self.vm.value_stack.push([])
        return True

    def op_RESPOND(self, opcode):
        self.vm.registers.ip += 3
        val = self.vm.value_stack.pop()
        print(f"[HTTP RESPONSE] {val}")
        return True"""

import re
code = re.sub(r"    def op_DB_INSERT.*?return True", patch, code, flags=re.DOTALL)

with open("runtime/vm/interpreter.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Interpreter patched!")

