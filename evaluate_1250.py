import json
import math
from collections import Counter
import time

class ExactDictionary:
    def __init__(self):
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

class TfIdfDictionary:
    def __init__(self):
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
        
        self.doc_counts = Counter()
        self.num_docs = len(self.classes)
        
        for class_name, keywords in self.classes.items():
            unique_words = set(keywords)
            for w in unique_words:
                self.doc_counts[w] += 1
                
        self.idf = {w: math.log(self.num_docs / (1 + count)) for w, count in self.doc_counts.items()}
        
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
                
        if best_score < 0.01:
            return "Unknown Specification"
            
        return best_class

def run_evaluation():
    with open('benchmark_v2_1250.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    exact_engine = ExactDictionary()
    tfidf_engine = TfIdfDictionary()
    
    results = []
    
    exact_passed = 0
    tfidf_passed = 0
    
    print("Evaluating 1,250 prompts...")
    start_time = time.time()
    
    for item in dataset:
        prompt = item['prompt']
        expected = item['expected']
        
        exact_pred = exact_engine.parse_intent(prompt)
        tfidf_pred = tfidf_engine.parse_intent(prompt)
        
        exact_is_pass = (exact_pred == expected)
        tfidf_is_pass = (tfidf_pred == expected)
        
        if exact_is_pass: exact_passed += 1
        if tfidf_is_pass: tfidf_passed += 1
        
        results.append({
            "prompt": prompt,
            "expected": expected,
            "exact_prediction": exact_pred,
            "exact_pass": exact_is_pass,
            "tfidf_prediction": tfidf_pred,
            "tfidf_pass": tfidf_is_pass
        })
        
    end_time = time.time()
    
    total = len(dataset)
    metrics = {
        "total_prompts": total,
        "exact_pass_rate": (exact_passed / total) * 100,
        "tfidf_pass_rate": (tfidf_passed / total) * 100,
        "time_taken_sec": end_time - start_time
    }
    
    # Save results
    with open('eval_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
        
    with open('eval_predictions.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    print("\n=== EVALUATION COMPLETE ===")
    print(f"Total Prompts: {metrics['total_prompts']}")
    print(f"Exact Dictionary Pass@1: {metrics['exact_pass_rate']:.1f}%")
    print(f"TF-IDF Baseline Pass@1: {metrics['tfidf_pass_rate']:.1f}%")
    print(f"Time Taken: {metrics['time_taken_sec']:.2f}s")
    print("Saved to eval_metrics.json and eval_predictions.json")

if __name__ == "__main__":
    run_evaluation()
