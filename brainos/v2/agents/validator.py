"""
=============================================================================
FILE: validator.py
PURPOSE: ValidatorAgent for BrainOS v2 Pipeline
=============================================================================
"""

from typing import Dict, Any

class ValidatorAgent:
    """
    ValidatorAgent performs readiness checks on the optimized architecture.
    It acts as a gatekeeper before handing over to the Executor, ensuring
    no malformed states exist.
    """
    def __init__(self):
        pass
        
    def execute(self, optimized_data: Dict[str, Any]) -> bool:
        print("[ValidatorAgent] Validating architecture readiness...")
        
        architecture = optimized_data.get("architecture", {})
        modules = architecture.get("modules", {})
        
        # Validation checks
        if not modules:
            print("[ValidatorAgent] Error: No modules generated in architecture.")
            return False
            
        if "api" in modules and "database" not in modules:
            # Maybe a warning, but let's allow stateless APIs. 
            pass
            
        if "folder_structure" not in architecture:
            print("[ValidatorAgent] Error: Folder structure missing from architecture.")
            return False
            
        print("[ValidatorAgent] Validation successful. Architecture is sound.")
        return True
