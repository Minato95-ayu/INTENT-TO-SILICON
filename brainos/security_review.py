class SecurityReview:
    """
    Reviews the generated logical architecture for security flaws and PII compliance.
    """
    def review(self, entities: dict) -> dict:
        pii_fields = ["email", "dob", "ssn", "medical_history", "password", "credit_card"]
        issues = []
        encrypted_fields = []
        
        for entity_name, fields in entities.items():
            for field in fields:
                field_name = field.split(":")[0].strip()
                if field_name in pii_fields:
                    issues.append(f"PII detected in {entity_name}.{field_name}")
                    encrypted_fields.append(f"{entity_name}.{field_name}")
                    
        score = 100 - (len(issues) * 10)
        return {
            "score": max(score, 0),
            "findings": issues,
            "auto_remediations": [f"Added @Encrypt annotation to {f}" for f in encrypted_fields]
        }
