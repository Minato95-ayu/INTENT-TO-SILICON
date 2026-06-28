from typing import Dict, Any, List
import json

class IntentModel:
    def __init__(self, domain: str):
        self.domain = domain
        self.entities = []
        self.features = []

    def add_entity(self, name: str):
        self.entities.append(name)
        
    def add_feature(self, feature: str):
        self.features.append(feature)
        
    def print_preview(self):
        print("\n--- Architecture Preview ---")
        print(f"Domain: {self.domain.capitalize()}")
        print("Entities:")
        for e in self.entities:
            print(f"  - {e}")
        print("Features:")
        for f in self.features:
            print(f"  - {f}")
        print("----------------------------\n")
        
    def to_aayu(self) -> str:
        lines = []
        # Use statements
        lines.append("use http.")
        lines.append("use db.")
        lines.append("")
        
        # We model entities as records
        for e in self.entities:
            lines.append(f"record {e}.")
            if e == "Patient":
                lines.append("    name")
                lines.append("    phone")
            elif e == "Doctor":
                lines.append("    name")
            lines.append("end.")
            lines.append("")
            
        # We can model pages/features as tasks for now
        if "Patient Dashboard" in self.features:
            lines.append("task setup_dashboard.")
            lines.append("    show \"Hospital\".")
            lines.append("    show \"Welcome Patient\".")
            lines.append("end.")
            lines.append("")
            
        return "\n".join(lines)

class IntentEngine:
    @staticmethod
    def build_from_answers(domain: str, answers: Dict[str, Any]) -> IntentModel:
        model = IntentModel(domain)
        
        # In a real scenario, this would map generic answers to architectural concepts.
        if domain == "hospital":
            model.add_entity("Hospital")
            if answers.get("doctor_login"):
                model.add_entity("Doctor")
                model.add_feature("Authentication (Doctor)")
            if answers.get("patient_portal"):
                model.add_entity("Patient")
                model.add_feature("Authentication (Patient)")
                model.add_feature("Patient Dashboard")
            
            branches = answers.get("branches")
            if branches == "Multi":
                model.add_entity("Branch")
                model.add_feature("Multi-tenancy")
                
        return model
