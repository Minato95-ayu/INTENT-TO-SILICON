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

class SchemaEngine:
    def __init__(self, models):
        self.models = models
        
    def build_schema_ir(self):
        schema_ir = {}
        for model in self.models:
            name = model["name"]
            fields = {f["name"]: f["type"] for f in model["fields"]}
            schema_ir[name] = fields
        return schema_ir
