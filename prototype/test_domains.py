import os
import builtins
import shutil

DOMAINS = [
    "Build a College LMS",
    "Build a Hospital Management System",
    "Build an E-commerce Platform",
    "Build a CRM"
]

def clean_output():
    if os.path.exists("main.aayu"):
        os.remove("main.aayu")
    if os.path.exists("views"):
        shutil.rmtree("views")

def run_test():
    import intent_engine.builder as builder
    
    success_count = 0

    print("--- AAYU Intent Engine v3 Bulk Test ---")
    for prompt in DOMAINS:
        print(f"\n[Testing Domain]: {prompt}")
        clean_output()
        
        # Reset mock answers for each run
        answers = ["yes", "yes", "yes", "yes", "yes", "yes"]
        def mock_input(p):
            return answers.pop(0) if answers else "yes"
        
        builtins.input = mock_input
        
        try:
            builder.build_app(prompt)
            
            # Verify Files exist
            if not os.path.exists("main.aayu"):
                raise Exception("main.aayu was not generated")
                
            if not os.path.exists("views") or len(os.listdir("views")) == 0:
                raise Exception("views directory is empty or missing")
                
            print(f"  [SUCCESS] -> Generated {len(os.listdir('views'))} UI templates and main.aayu.")
            success_count += 1
            
        except Exception as e:
            print(f"  [FAILED] -> {str(e)}")
            
    print(f"\nResults: {success_count}/{len(DOMAINS)} Domains Passed.")

if __name__ == "__main__":
    run_test()
