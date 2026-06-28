import os
import json
import sys

def build(filepath: str, base_out_dir: str):
    """
    The single source of truth for the AAYU compilation and generation pipeline.
    """
    # Ensure modules can be imported
    cli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cli_dir)
    sys.path.insert(0, os.path.join(cli_dir, "aayu_language"))

    from aayu_language.lexer import Lexer
    from aayu_language.parser import Parser
    from aayu_language.ir_generator import generate_ir
    from target_engine.scorer import select_target

    print("Validating...")
    # 1. Parse & IR
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
        
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize(), filename=filepath)
    ast = parser.parse()
    ir_json_str = generate_ir(ast)
    ir_data = json.loads(ir_json_str)
    
    print("[OK] Syntax Valid")
    print("Generating Architecture...")
    
    # 2. Target Selection
    target_plan_json = select_target(ir_data)
    target_plan = json.loads(target_plan_json)
    
    # 3. Generate Code
    generators = target_plan.get("generators", [])
    
    if "react-generator" in generators:
        from generators.react.generator import ReactGenerator
        out_dir = os.path.join(base_out_dir, "frontend")
        react_gen = ReactGenerator(ir_data, out_dir)
        react_gen.generate()
        print("[OK] React")
        
    if "fastapi-generator" in generators:
        from generators.fastapi.generator import FastAPIGenerator
        out_dir = os.path.join(base_out_dir, "backend")
        fastapi_gen = FastAPIGenerator(ir_data, out_dir)
        fastapi_gen.generate()
        print("[OK] FastAPI")
        
    if "postgresql-generator" in generators or "postgres-generator" in generators:
        from generators.postgres.generator import PostgresGenerator
        out_dir = os.path.join(base_out_dir, "database")
        pg_gen = PostgresGenerator(ir_data, out_dir)
        pg_gen.generate()
        print("[OK] PostgreSQL")
        
    # Orchestrator
    from generators.orchestrator.generator import OrchestratorGenerator
    orch_gen = OrchestratorGenerator(ir_data, base_out_dir)
    orch_gen.generate()
