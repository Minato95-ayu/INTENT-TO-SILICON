"""
=============================================================================
FILE: test_multi_intent.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'prototype', 'compiler_v2'))

from normalizer import Normalizer
from pain_point_extractor import PainPointExtractor
from intent_graph import IntentGraphBuilder
from workflow_generator import SemanticWorkflowGenerator

def run_multi_intent_test():
    normalizer = Normalizer()
    extractor = PainPointExtractor()
    graph_builder = IntentGraphBuilder()
    workflow_gen = SemanticWorkflowGenerator()
    
    print("=== Aayu Multi-Intent Compiler Verification ===")
    test_phrase = "mera upi fail ho gaya, screen freeze ho gayi, customer care reply nahi de raha"
    print(f"\nInput: {test_phrase}")
    
    # 1. Normalize
    normalized = normalizer.normalize(test_phrase)
    
    # 2. Extract All Intents
    intents = extractor.extract_all(normalized)
    print("\n--- Intent IR (Multiple) ---")
    simplified_intents = [{"domain": i["module"], "problem": i["primary_problem"]} for i in intents]
    print(json.dumps(simplified_intents, indent=2))
    
    # 3. Build Intent Graph (Topological Sort)
    graph = graph_builder.build_graph(intents)
    print("\n--- Intent Graph (Topological Order) ---")
    for idx, node in enumerate(graph):
        print(f"{idx+1}. [{node['domain']}] {node['problem']}")
        
    # 4. Generate Semantic Workflow YAML
    workflow_yaml = workflow_gen.generate(graph)
    print("\n--- Generated YAML Workflow ---")
    print(workflow_yaml)

if __name__ == "__main__":
    run_multi_intent_test()
