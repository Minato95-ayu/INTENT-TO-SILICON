import sys
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from normalizer import Normalizer
from pain_point_extractor import PainPointExtractor
from intent_graph import IntentGraphBuilder
from workflow_generator import SemanticWorkflowGenerator
from resolution_engine import ResolutionEngine

def run_resolution_test():
    normalizer = Normalizer()
    extractor = PainPointExtractor()
    graph_builder = IntentGraphBuilder()
    workflow_gen = SemanticWorkflowGenerator()
    resolver = ResolutionEngine()
    
    print("=== Aayu Resolution Engine Verification ===")
    test_phrase = "mera upi fail ho gaya, screen freeze ho gayi, customer care reply nahi de raha"
    print(f"\nInput: {test_phrase}")
    
    # 1. Normalize
    normalized = normalizer.normalize(test_phrase)
    
    # 2. Extract All Intents
    intents = extractor.extract_all(normalized)
    
    # 3. Build Intent Graph (Topological Sort)
    graph = graph_builder.build_graph(intents)
        
    # 4. Generate Semantic Workflow YAML
    workflow_yaml = workflow_gen.generate(graph)
    print("\n--- 1. Semantic Workflow ---")
    print(workflow_yaml)
    
    # 5. Reasoning Layer (Resolution Engine)
    print("--- 2. Reasoning Layer Output ---")
    resolutions = resolver.generate_candidates(workflow_yaml)
    print(json.dumps(resolutions, indent=2))

if __name__ == "__main__":
    run_resolution_test()
