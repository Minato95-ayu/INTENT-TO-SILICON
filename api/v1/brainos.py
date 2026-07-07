from fastapi import APIRouter
from .models import BrainOSRequest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# We simulate the complex multi-domain output from the actual engine
from prototype.ai.brainos import BrainOS
from prototype.ai.intent_engine import IntentEngine

router = APIRouter()

@router.post("/brainos")
def generate_architecture(request: BrainOSRequest):
    try:
        # First process intent through NLP
        engine = IntentEngine()
        ir = engine.parse_intent(request.intent)
        
        # Then generate architecture through BrainOS
        brainos = BrainOS()
        # In a real environment, brainos.generate would take the IR directly and return rich objects.
        # We will mock the output shape requested by the UI since the console version does prints.
        
        return {
            "success": True,
            "architecture": {
                "name": "Generated Architecture",
                "components": ir.get("entities", [])
            },
            "recommendations": [
                "Use Edge Caching for high read throughput.",
                "Implement a Read Replica for the database."
            ],
            "tradeoffs": [
                "Higher eventual consistency due to read replicas.",
                "Increased cost due to edge cache nodes."
            ],
            "folder_structure": [
                "src/",
                "src/main.aayu",
                "src/models/",
                "tests/"
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
