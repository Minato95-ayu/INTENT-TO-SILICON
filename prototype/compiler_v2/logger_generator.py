"""
Aayu Logger Generator (Sprint 37)

Generates a structured JSON logger for the FastAPI backend.
"""

import os
from .schema_nodes import SchemaModel

class LoggerGenerator:
    def __init__(self, schema: SchemaModel, output_dir: str):
        self.schema = schema
        self.output_dir = output_dir

    def generate(self):
        logger_path = os.path.join(self.output_dir, "logger.py")
        
        # We generate a simple wrapper around Python's logging that formats output as JSON
        content = f"""import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {{
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }}
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
        if hasattr(record, "entity"):
            log_record["entity"] = record.entity
        if hasattr(record, "action"):
            log_record["action"] = record.action
            
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    return logger
"""
        with open(logger_path, "w") as f:
            f.write(content)
        
        return True
