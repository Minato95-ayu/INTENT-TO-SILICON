import subprocess
import os
from intent_engine.parser import IntentParser
from intent_engine.graph import IntentGraph
from intent_engine.verifier import VerificationEngine
from intent_engine.generator import AayuGenerator

def test_intent_engine():
    print("--- 1. Raw Human Thought ---")
    sentences = [
        "Make a student record",
        "Add name to student",
        "Add age to student",
        "Create a Library entity",
        "Add owner to library",
        "Add books to library"
    ]
    for s in sentences:
        print(f"User: {s}")

    print("\n--- 2. Intent Graph ---")
    parser = IntentParser()
    graph = IntentGraph()
    for sentence in sentences:
        intent = parser.parse(sentence)
        if intent:
            graph.ingest(intent)
            
    for entity, data in graph.get_snapshot().items():
        print(f"{entity}")
        for i, field in enumerate(data["fields"]):
            prefix = "  \\-- " if i == len(data["fields"]) - 1 else "  |-- "
            print(f"{prefix}{field}")

    print("\n--- 3. Architecture Verification ---")
    verifier = VerificationEngine()
    report = verifier.verify(graph)
    print(f"Status: {report.status}")
    print(f"Score: {report.score}")
    print(f"Confidence: {report.confidence}%")
    
    print("\n--- 4. Aayu Generator ---")
    generator = AayuGenerator()
    try:
        result = generator.generate(graph, report)
        print("Generation Metadata:")
        print(f"  Entities Generated: {result.metadata['entities_generated']}")
        for ent, count in result.metadata['entity_details'].items():
            print(f"    {ent}: {count} fields")
            
        print("\nGenerated Aayu Source:")
        print("----------------------")
        print(result.code.strip())
        print("----------------------")
        
        # Write to file for execution
        file_path = os.path.join("aayu_language", "examples", "generated_app.aayu")
        with open(file_path, "w") as f:
            f.write(result.code)
            
        print("\n--- 5. Aayu Runtime Execution ---")
        print(f"Executing: python aayu_language/run.py {file_path}")
        out = subprocess.run(["python", "aayu_language/run.py", file_path], capture_output=True, text=True)
        if out.returncode == 0:
            print("SUCCESS: Aayu Runtime successfully parsed and loaded the generated source code!")
            if out.stdout.strip():
                print(out.stdout)
        else:
            print("EXECUTION FAILED:")
            print(out.stderr)
            
    except Exception as e:
        print(f"\n[BLOCKED] {e}")

if __name__ == "__main__":
    test_intent_engine()
