import sys
from intent_ir import IntentIR

def run_demo():
    print("🚀 Intent Engine Demo")
    print("----------------------")
    
    intent = "Build a global CRM system with high read throughput"
    if len(sys.argv) > 1:
        intent = sys.argv[1]
        
    print(f"\n[Input Intent]: {intent}\n")
    
    ir = IntentIR()
    result = ir.to_json(intent)
    
    print("[Output Intent IR]:")
    print(result)

if __name__ == '__main__':
    run_demo()
