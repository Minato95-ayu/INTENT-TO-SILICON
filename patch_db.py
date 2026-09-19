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

with open("runtime/stdlib/modules/database_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

new_func = '''
    def fn_execute(args, vm):
        try:
            cid = args[0].to_python()
            query = args[1].to_python()
            conn = connections.get(cid)
            if not conn: return NumberValue(0)
            
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return NumberValue(float(cursor.rowcount))
        except Exception as e:
            return NumberValue(-1)
            
    registry.register("db::execute", fn_execute)
    registry.register("db::connect", fn_connect)
'''
content = content.replace('    registry.register("db::connect", fn_connect)', new_func)

with open("runtime/stdlib/modules/database_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated database_lib")
