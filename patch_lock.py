# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re
with open("runtime/plugins/storage/runtime.py", "r") as f:
    c = f.read()

patch = """    def _execute(self, sql: str, params: tuple = (), commit: bool = False, transaction_id: str = None) -> Any:
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            if commit:
                self.conn.commit()
            rows_affected = cursor.rowcount
            
            # If it's a SELECT, return rows
            if sql.strip().upper().startswith("SELECT"):
                return [dict(r) for r in cursor.fetchall()], rows_affected
            else:
                return None, rows_affected"""

c = re.sub(r'    def _execute\(self, sql: str, params: tuple = \(\), commit: bool = False, transaction_id: str = None\) -> Any:.*?return None, rows_affected', patch, c, flags=re.DOTALL)
with open("runtime/plugins/storage/runtime.py", "w") as f:
    f.write(c)
