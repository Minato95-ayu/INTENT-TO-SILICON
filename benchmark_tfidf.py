import csv
import math
from collections import Counter

class TfIdfDictionary:
    def __init__(self):
        # We expand the dictionary corpus to represent the 'training' knowledge
        self.classes = {
            "Latency < 200ms": ["fast", "response", "tezi", "load", "lag", "turant", "jaldi", "speed", "quick"],
            "AES-256 Encryption": ["safe", "data", "secure", "hack", "leak", "risk", "security", "encryption"],
            "Auto-scaling": ["public", "lakhon", "traffic", "server", "down", "load", "heavy", "scale", "users"],
            "RBAC / Admin Only": ["main", "dekh", "backend", "admin", "section", "control", "sirf", "mujhe", "access"],
            "Resource-constrained footprint": ["chhota", "size", "memory", "low", "end", "halka", "footprint", "space"],
            "WebSockets": ["real-time", "update", "message", "instantly", "live", "chatting", "sync", "socket"],
            "Public Access": ["login", "nahi", "account", "otp", "password", "open", "all", "sab", "public"],
            "Offline Support": ["bina", "internet", "net", "airplane", "mode", "connection", "locally", "offline", "save"],
            "SQLite": ["sasta", "database", "paise", "kharchne", "local", "db", "sqlite"],
            "Admin Portal": ["admin", "dashboard", "manage", "panel", "peeche", "setup", "sales", "track", "screen"]
        }
        
        # Build IDF
        self.doc_counts = Counter()
        self.num_docs = len(self.classes)
        
        for class_name, keywords in self.classes.items():
            unique_words = set(keywords)
            for w in unique_words:
                self.doc_counts[w] += 1
                
        self.idf = {w: math.log(self.num_docs / (1 + count)) for w, count in self.doc_counts.items()}
        
        # Build TF-IDF vectors for classes
        self.class_vectors = {}
        for class_name, keywords in self.classes.items():
            self.class_vectors[class_name] = self._compute_tfidf(keywords)
            
    def _compute_tfidf(self, words):
        tf = Counter(words)
        vec = {}
        for w, count in tf.items():
            if w in self.idf:
                vec[w] = (count / len(words)) * self.idf[w]
        return vec
        
    def _cosine_similarity(self, vec1, vec2):
        dot = sum(vec1.get(w, 0) * vec2.get(w, 0) for w in set(vec1) | set(vec2))
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)

    def parse_intent(self, prompt: str) -> str:
        prompt_words = prompt.lower().split()
        prompt_vec = self._compute_tfidf(prompt_words)
        
        best_score = 0.0
        best_class = "Unknown Specification"
        
        for class_name, class_vec in self.class_vectors.items():
            score = self._cosine_similarity(prompt_vec, class_vec)
            if score > best_score:
                best_score = score
                best_class = class_name
                
        # Safety Halting Threshold (If confidence is too low)
        if best_score < 0.01:
            return "Unknown Specification"
            
        return best_class

def run_benchmark():
    print("=== AAYU INTENT ENGINE BENCHMARK (TF-IDF BASELINE) ===\n")
    engine = TfIdfDictionary()
    
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
