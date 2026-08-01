import json

class OpenAPIGenerator:
    def __init__(self, db_models, action_params=None):
        self.db_models = db_models
        self.action_params = action_params or {}

    def generate(self):
        doc = {
            "openapi": "3.1.0",
            "info": {
                "title": "AAYU Generated API",
                "version": "1.0.0",
                "description": "Auto-generated OpenAPI specification for AAYU application.",
                "license": {"name": "MIT"},
                "contact": {"name": "AAYU Developer"}
            },
            "servers": [
                {"url": "http://localhost:8000"}
            ],
            "tags": [],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                },
                "responses": {},
                "parameters": {}
            }
        }

        for model_name in self.db_models:
            doc["tags"].append({"name": model_name})
            
        if self.action_params:
            doc["tags"].append({"name": "Actions"})

        for model_name, model_info in self.db_models.items():
            schema = self._generate_schema(model_name, model_info)
            doc["components"]["schemas"][model_name] = schema
            
            partial_schema = self._generate_schema(model_name, model_info, partial=True)
            doc["components"]["schemas"][f"{model_name}Update"] = partial_schema
            
            self._generate_crud_paths(doc["paths"], model_name, model_info)

        for action_name, params in self.action_params.items():
            # Action path e.g. /api/login
            path = f"/api/{action_name}"
            doc["paths"][path] = {
                "post": {
                    "tags": ["Actions"],
                    "summary": f"Execute {action_name}",
                    "operationId": action_name,
                    "responses": {
                        "200": {"description": "Action executed successfully"}
                    }
                }
            }

        return doc

    def _get_example_value(self, field_name, f_type, format_):
        if format_ == "email": return "user@example.com"
        if format_ == "uuid": return "123e4567-e89b-12d3-a456-426614174000"
        if format_ == "uri": return "https://example.com"
        
        if f_type == "string":
            if "name" in field_name.lower(): return "John Doe"
            return "string"
        if f_type == "integer": return 1
        if f_type == "number": return 1.5
        if f_type == "boolean": return True
        return None

    def _generate_schema(self, model_name, model_info, partial=False):
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        schema["properties"]["id"] = {"type": "integer", "readOnly": True, "example": 1}
        schema["properties"]["created_at"] = {"type": "string", "format": "date-time", "readOnly": True}
        schema["properties"]["updated_at"] = {"type": "string", "format": "date-time", "readOnly": True}

        example = {"id": 1, "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z"}

        for field_name, meta in model_info["fields"].items():
            prop = {}
            
            t = meta["type"]
            f_type = "string"
            format_ = None
            if t == "Int": f_type = "integer"
            elif t == "Float": f_type = "number"
            elif t == "Boolean": f_type = "boolean"
            elif t == "Email": 
                f_type = "string"
                format_ = "email"
            elif t == "UUID":
                f_type = "string"
                format_ = "uuid"
            elif t == "URL":
                f_type = "string"
                format_ = "uri"
            elif t == "DateTime":
                f_type = "string"
                format_ = "date-time"
            elif t == "Date":
                f_type = "string"
                format_ = "date"
                
            prop["type"] = f_type
            if format_: prop["format"] = format_
            
            if meta["nullable"]:
                prop["type"] = [f_type, "null"]

            if meta["min"] is not None:
                if f_type == "string": prop["minLength"] = int(meta["min"])
                else: prop["minimum"] = float(meta["min"])
                
            if meta["max"] is not None:
                if f_type == "string": prop["maxLength"] = int(meta["max"])
                else: prop["maximum"] = float(meta["max"])
                
            if meta["regex"]:
                prop["pattern"] = meta["regex"]
                
            if meta["enum"]:
                prop["enum"] = meta["enum"]
                
            if meta["default"]:
                prop["default"] = meta["default"]
                
            example_val = self._get_example_value(field_name, f_type, format_)
            if example_val is not None:
                prop["example"] = example_val
                example[field_name] = example_val

            schema["properties"][field_name] = prop
            
            if not partial and meta["required"]:
                schema["required"].append(field_name)
                
        if not schema["required"]:
            schema.pop("required")
            
        schema["example"] = example
        return schema

    def _generate_crud_paths(self, paths, model_name, model_info):
        base_path = f"/api/{model_name.lower()}s"
        item_path = f"/api/{model_name.lower()}s/{{id}}"
        
        security = []
        if model_info.get("secure", False):
            security = [{"bearerAuth": []}]
            
        paths[base_path] = {
            "get": {
                "tags": [model_name],
                "summary": f"List {model_name}s",
                "operationId": f"list{model_name}s",
                "security": security,
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": f"#/components/schemas/{model_name}"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": [model_name],
                "summary": f"Create {model_name}",
                "operationId": f"create{model_name}",
                "security": security,
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{model_name}"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": f"#/components/schemas/{model_name}"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Validation Error"}
                }
            },
            "head": {
                "tags": [model_name],
                "summary": f"Check {model_name}s headers",
                "operationId": f"head{model_name}s",
                "security": security,
                "responses": {"200": {"description": "Successful Response"}}
            },
            "options": {
                "tags": [model_name],
                "summary": f"{model_name}s options",
                "operationId": f"options{model_name}s",
                "security": security,
                "responses": {"200": {"description": "Successful Response"}}
            }
        }
        
        paths[item_path] = {
            "get": {
                "tags": [model_name],
                "summary": f"Get {model_name} by ID",
                "operationId": f"get{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": f"#/components/schemas/{model_name}"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {"description": "Not Found"}
                }
            },
            "put": {
                "tags": [model_name],
                "summary": f"Update {model_name} (Full)",
                "operationId": f"update{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{model_name}"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": f"#/components/schemas/{model_name}"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Validation Error"},
                    "404": {"description": "Not Found"}
                }
            },
            "patch": {
                "tags": [model_name],
                "summary": f"Update {model_name} (Partial)",
                "operationId": f"patch{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{model_name}Update"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"$ref": f"#/components/schemas/{model_name}"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Validation Error"},
                    "404": {"description": "Not Found"}
                }
            },
            "delete": {
                "tags": [model_name],
                "summary": f"Delete {model_name}",
                "operationId": f"delete{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "data": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {"description": "Not Found"}
                }
            },
            "head": {
                "tags": [model_name],
                "summary": f"Check {model_name}",
                "operationId": f"head{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {"200": {"description": "Successful Response"}, "404": {"description": "Not Found"}}
            },
            "options": {
                "tags": [model_name],
                "summary": f"{model_name} options",
                "operationId": f"options{model_name}",
                "security": security,
                "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                "responses": {"200": {"description": "Successful Response"}, "404": {"description": "Not Found"}}
            }
        }
