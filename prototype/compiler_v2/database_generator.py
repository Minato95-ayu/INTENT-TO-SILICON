import os
import json

class DatabaseGenerator:
    def __init__(self):
        pass

    def _type_to_sqlalchemy(self, sql_type):
        sql_type = sql_type.upper()
        if "UUID" in sql_type: return "String" # using String for SQLite compatibility prototype
        if "VARCHAR" in sql_type: return "String"
        if "INT" in sql_type: return "Integer"
        if "BOOLEAN" in sql_type: return "Boolean"
        if "TIMESTAMP" in sql_type or "DATE" in sql_type: return "DateTime"
        if "DECIMAL" in sql_type: return "Float"
        return "String"

    def generate_database_setup(self):
        return """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Development: SQLite, Production: PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./aayu_generated.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

    def generate_models(self, resolved_schema):
        models_code = "from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime\n"
        models_code += "from sqlalchemy.orm import relationship\n"
        models_code += "import datetime\n"
        models_code += "import uuid\n"
        models_code += "from database import Base\n\n"
        
        for entity, definition in resolved_schema.items():
            model_name = ''.join(word.title() for word in entity.split('_'))
            models_code += f"class {model_name}(Base):\n"
            models_code += f"    __tablename__ = '{entity}'\n\n"
            
            for field in definition.get("fields", []):
                sa_type = self._type_to_sqlalchemy(field["type"])
                
                args = [sa_type]
                if field.get("primary_key"):
                    args.append("primary_key=True")
                    args.append("index=True")
                    args.append("default=lambda: str(uuid.uuid4())")
                if field.get("unique"):
                    args.append("unique=True")
                if field.get("foreign_key"):
                    ref_table, ref_col = field["foreign_key"].split('.')
                    args.append(f"ForeignKey('{ref_table}.{ref_col}')")
                
                # Handling defaults
                if field.get("default") == "CURRENT_TIMESTAMP":
                    args.append("default=datetime.datetime.utcnow")
                elif field.get("default") == "'ACTIVE'":
                    args.append("default='ACTIVE'")
                elif field.get("default") == "'PENDING'":
                    args.append("default='PENDING'")
                elif field.get("default") == "'APPLIED'":
                    args.append("default='APPLIED'")
                elif field.get("default") == "'UPI'":
                    args.append("default='UPI'")
                elif field.get("default") == "'INR'":
                    args.append("default='INR'")
                elif field.get("default") == "TRUE":
                    args.append("default=True")
                elif field.get("default") == "2":
                    args.append("default=2")
                
                args_str = ", ".join(args)
                models_code += f"    {field['name']} = Column({args_str})\n"
                
            models_code += "\n"
            
        return models_code
