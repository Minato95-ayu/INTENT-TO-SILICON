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
