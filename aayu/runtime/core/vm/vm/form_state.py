class FormStateManager:
    """Manages form state natively in the Virtual Machine."""
    def __init__(self, vm):
        self.vm = vm

    def init_form(self, form_name="$form"):
        """Initializes a new form state in the current scope."""
        scope = self.vm.state_scopes[-1]
        
        scope[form_name] = {
            "valid": True,
            "invalid": False,
            "dirty": False,
            "touched": False,
            "submitting": False,
            "values": {},
            "errors": {}
        }
        
    def get_form(self, form_name="$form"):
        for scope in reversed(self.vm.state_scopes):
            if form_name in scope:
                return scope[form_name]
        return None

    def set_rules(self, form_name, rules):
        form = self.get_form(form_name)
        if form:
            form["rules"] = rules
            print(f"[FormState] Rules set for {form_name}: {rules}")

    def validate_field(self, form_name, field_name, value):
        form = self.get_form(form_name)
        if not form or "rules" not in form:
            print(f"[FormState] No rules found for {form_name}")
            return True

        if field_name not in form["rules"]:
            return True

        field_rules = form["rules"][field_name]
        for rule_obj in field_rules:
            rule_type = rule_obj.get("rule")
            args = rule_obj.get("args", [])
            
            # Simple validation logic
            if rule_type == "required":
                if not value or str(value).strip() == "":
                    self.set_error(form_name, field_name, {"type": "required", "code": "REQUIRED", "message": "This field is required"})
                    return False
            elif rule_type == "email":
                if "@" not in str(value):
                    self.set_error(form_name, field_name, {"type": "email", "code": "INVALID_EMAIL", "message": "Invalid email address"})
                    return False
            elif rule_type == "minLength":
                min_len = int(args[0]) if args else 0
                if len(str(value)) < min_len:
                    self.set_error(form_name, field_name, {"type": "minLength", "code": "MIN_LENGTH", "message": f"Minimum {min_len} characters required"})
                    return False

        self.clear_error(form_name, field_name)
        return True

    def update_field(self, form_name, field_name, value):
        form = self.get_form(form_name)
        if form:
            form["values"][field_name] = value
            form["dirty"] = True
            form["touched"] = True
            self.validate_field(form_name, field_name, value)
            
    def set_error(self, form_name, field_name, error_dict):
        """error_dict example: {'type': 'required', 'code': 'REQUIRED', 'message': 'Email is required'}"""
        form = self.get_form(form_name)
        if form:
            form["errors"][field_name] = error_dict
            self.recalculate_validity(form_name)
            
    def clear_error(self, form_name, field_name):
        form = self.get_form(form_name)
        if form and field_name in form["errors"]:
            del form["errors"][field_name]
            self.recalculate_validity(form_name)
            
    def recalculate_validity(self, form_name):
        form = self.get_form(form_name)
        if form:
            form["valid"] = len(form["errors"]) == 0
            form["invalid"] = not form["valid"]
            
    def get_value(self, form_name, field_name):
        form = self.get_form(form_name)
        if form:
            return form["values"].get(field_name)
        return None
