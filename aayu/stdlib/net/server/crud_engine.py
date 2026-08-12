import re

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors

class CrudEngine:
    def __init__(self, db):
        self.db = db

    def _validate_payload(self, model_name: str, payload: dict, is_patch: bool = False):
        schema_fields = self.db.models[model_name]["fields"]
        errors = {}
        
        for field_name, rules in schema_fields.items():
            if field_name in ["id", "created_at", "updated_at"]:
                continue
                
            val = payload.get(field_name)
            
            # 1. Required Check
            if rules.get("required"):
                if val is None:
                    if not is_patch or field_name in payload: # PATCH ignores missing keys
                        errors.setdefault(field_name, []).append("Field is required")
                    continue
            
            if val is None:
                # 2. Default injection
                default = rules.get("default")
                if default is not None and not is_patch:
                    payload[field_name] = default
                    continue
                    
                # 3. Nullable check
                if not rules.get("nullable") and not is_patch:
                    errors.setdefault(field_name, []).append("Field cannot be null")
                continue
                
            # 4. Type Check
            f_type = rules.get("type")
            if f_type in ["Int", "Boolean"] and not isinstance(val, int):
                errors.setdefault(field_name, []).append("Must be an integer")
            elif f_type == "Float" and not isinstance(val, (int, float)):
                errors.setdefault(field_name, []).append("Must be a number")
            elif f_type == "String" and not isinstance(val, str):
                errors.setdefault(field_name, []).append("Must be a string")
                
            # 5. Min/Max
            if isinstance(val, str):
                if rules.get("min") is not None and len(val) < int(rules["min"]):
                    errors.setdefault(field_name, []).append(f"Minimum length is {rules['min']}")
                if rules.get("max") is not None and len(val) > int(rules["max"]):
                    errors.setdefault(field_name, []).append(f"Maximum length is {rules['max']}")
            elif isinstance(val, (int, float)):
                if rules.get("min") is not None and val < int(rules["min"]):
                    errors.setdefault(field_name, []).append(f"Minimum value is {rules['min']}")
                if rules.get("max") is not None and val > int(rules["max"]):
                    errors.setdefault(field_name, []).append(f"Maximum value is {rules['max']}")
                    
            # 6. Regex Check
            regex = rules.get("regex")
            if regex and isinstance(val, str):
                if not re.match(regex, val):
                    errors.setdefault(field_name, []).append("Invalid format")
                    
            # 7. Enum Check
            enum_vals = rules.get("enum")
            if enum_vals and val not in enum_vals:
                errors.setdefault(field_name, []).append(f"Must be one of {enum_vals}")

        if errors:
            raise ValidationError(errors)
            
    def create(self, model_name: str, payload: dict):
        self._validate_payload(model_name, payload, is_patch=False)
        return self.db.insert(model_name, payload)

    def read(self, model_name: str, record_id: int):
        return self.db.find_one(model_name, record_id)

    def list(self, model_name: str, query_params: dict):
        return self.db.find(model_name, query_params)

    def count(self, model_name: str, query_params: dict):
        return self.db.count(model_name, query_params)

    def update(self, model_name: str, record_id: int, payload: dict, partial: bool = False):
        self._validate_payload(model_name, payload, is_patch=partial)
        if partial:
            # For patch, we first get existing
            existing = self.db.find_one(model_name, record_id)
            if not existing:
                return None
            for k, v in payload.items():
                existing[k] = v
            # don't update ID or created_at
            if 'id' in existing: del existing['id']
            if 'created_at' in existing: del existing['created_at']
            if 'updated_at' in existing: del existing['updated_at']
            return self.db.update(model_name, record_id, existing)
        else:
            return self.db.update(model_name, record_id, payload)

    def delete(self, model_name: str, record_id: int):
        # For future: check if soft_delete is enabled on model
        return self.db.delete(model_name, record_id)
        
    def exists(self, model_name: str, record_id: int):
        return self.db.exists(model_name, record_id)
