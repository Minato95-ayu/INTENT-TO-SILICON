import csv

class SemanticDictionary:
    def __init__(self):
        # A simple deterministic dictionary mapping colloquial phrases to formal specs
        self.dictionary = {
            "fast": "Latency < 200ms",
            "safe": "AES-256 Encryption",
            "public": "Auto-scaling",
            "main dekh": "RBAC / Admin Only",
            "chhota": "Resource-constrained footprint",
            "real-time": "WebSockets",
            "login nahi": "Public Access",
            "bina internet": "Offline Support",
            "sasta database": "SQLite",
            "admin dashboard": "Admin Portal"
        }
        
    def parse_intent(self, prompt: str) -> str:
        prompt = prompt.lower()
        for key, spec in self.dictionary.items():
            if key in prompt:
                return spec
        return "Unknown Specification"

def run_benchmark():
    print("=== AAYU INTENT ENGINE BENCHMARK (REAL HELD-OUT DATA) ===\n")
    engine = SemanticDictionary()
    
    total_prompts = 0
    passed = 0
    
    with open('dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row['Prompt']
            expected = row['Expected']
            
            predicted = engine.parse_intent(prompt)
            is_pass = (predicted == expected)
            
            total_prompts += 1
            if is_pass:
                passed += 1
                status = "PASS"
            else:
                status = f"FAIL (Got: {predicted})"
                
            print(f"Prompt: '{prompt}'")
            print(f"Expected: {expected} | {status}\n")
            
    accuracy = (passed / total_prompts) * 100
    print("-" * 50)
    print(f"Total Prompts: {total_prompts}")
    print(f"Pass@1 Accuracy: {accuracy:.1f}%")
    print("-" * 50)

if __name__ == "__main__":
    run_benchmark()
