import os
from typing import Dict, Any

class PrismaGenerator:
    """
    Consumes App IR to generate Prisma schema and database configuration.
    """
    def __init__(self, ir: Dict[str, Any], output_dir: str = "backend/prisma"):
        self.ir = ir
        self.output_dir = output_dir

    def generate(self):
        data_ir = self.ir.get("data_ir", {})
        models = data_ir.get("models", [])
        storages = data_ir.get("storages", [])
        
        if not models and not storages:
            return  # Nothing to generate
            
        os.makedirs(self.output_dir, exist_ok=True)
        
        provider = "sqlite" # Default
        url = 'env("DATABASE_URL")'
        
        schema = f"""// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "{provider}"
  url      = {url}
}}

"""
        
        # We can map AAYU types to Prisma types
        type_mapping = {
            "Int": "Int",
            "String": "String",
            "Boolean": "Boolean",
            "number": "Float",
            "text": "String"
        }

        for model in models:
            schema += f"model {model['name']} {{\n"
            has_id = False
            for field in model["fields"]:
                fname = field["name"]
                ftype = field["type"]
                
                # Check for array
                is_array = False
                if ftype.endswith("[]"):
                    is_array = True
                    ftype = ftype[:-2]
                    
                prisma_type = type_mapping.get(ftype, ftype)
                if is_array:
                    prisma_type += "[]"
                    
                line = f"  {fname} {prisma_type}"
                if fname == "id" and not has_id:
                    if prisma_type == "Int":
                        line += " @id @default(autoincrement())"
                    else:
                        line += " @id @default(uuid())"
                    has_id = True
                schema += f"{line}\n"
            schema += "}\n\n"
            
        with open(os.path.join(self.output_dir, "schema.prisma"), "w", encoding="utf-8") as f:
            f.write(schema)
