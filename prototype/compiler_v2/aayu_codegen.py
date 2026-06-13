class PythonGenerator:
    def generate(self, aayu_ir):
        """
        Converts Aayu IR to a Python conditional block.
        """
        if not aayu_ir:
            return ""
            
        event = aayu_ir.get("event")
        condition = aayu_ir.get("condition")
        action = aayu_ir.get("action")
        
        if not event or not condition or not action:
            return ""
            
        # Example: 
        # event: payment_debited
        # condition: order_missing
        # action: trigger_refund
        
        # We want to format the condition appropriately. 
        # For simplicity, we just use the raw strings, but we can do some basic parsing.
        # e.g., 'order_missing' -> 'not order_created' if it ends in '_missing'
        
        parsed_condition = condition
        if condition.endswith("_missing"):
            base = condition.replace("_missing", "")
            parsed_condition = f"not {base}_created"
        
        code = f"if {event} and {parsed_condition}:\n"
        code += f"    {action}()"
        
        return code
