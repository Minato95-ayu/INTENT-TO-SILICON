import json
import random

# Seed for reproducibility
random.seed(42)

PREFIXES = ["Mujhe", "Mera", "App me", "Bhai", ""]
SUFFIXES = ["chahiye", "kar do", "zaroori hai", "mangta hai", "laga dena"]

CORES = {
    "Latency < 200ms": [
        "app bahot tezi se load hona",
        "bina lag ke turant page khul jaye",
        "jaldi reply aana",
        "speed ekdum lightning fast hona",
        "koi loading screen nahi dikhna"
    ],
    "AES-256 Encryption": [
        "koi bhi hack na kar paye mere data ko",
        "information secure rehni",
        "data leak ka risk zero hona",
        "end to end encryption hona",
        "security sabse tight rehna"
    ],
    "Auto-scaling": [
        "kal ko lakhon log aayenge app par handle hona",
        "traffic badhne par server down nahi hona",
        "heavy load aaram se handle kar sake",
        "lakho users ek sath aaye to crash nahi hona",
        "scale karne me issue nahi aana"
    ],
    "RBAC / Admin Only": [
        "sirf mujhe hi backend dikhna",
        "users ko admin section mat dikhana",
        "kaun kya dekh sakta hai uspe control",
        "role ke hisaab se page block hona",
        "admin power sirf selected logo ko milna"
    ],
    "Resource-constrained footprint": [
        "app ka size bahot chhota rakhna",
        "kam memory me chalne wala code likhna",
        "low end mobile pe bhi chal jana",
        "halka phulka apk banna",
        "storage zyada nahi lena"
    ],
    "WebSockets": [
        "jaise hi koi message kare instantly dikhna",
        "live chatting feature",
        "real time data sync hona",
        "live tracking map dikhna",
        "page refresh ke bina update aana"
    ],
    "Public Access": [
        "sab log bina account ke dekh sakein",
        "koi OTP ya password nahi mangna",
        "open for all rakhna hai isko",
        "login page hata dena",
        "bina register kiye sab accessible hona"
    ],
    "Offline Support": [
        "agar net chala jaye to bhi app kaam kare",
        "airplane mode me bhi details dikhe",
        "no connection me data locally save ho jaye",
        "offline mode add karna",
        "bina internet ke bhi load hona"
    ],
    "SQLite": [
        "sasta aur halka data store karke rakho",
        "database ke liye zyada paise nahi kharchne",
        "local DB me kaam chala lo",
        "phone ke storage me hi save karna",
        "server ka cost bachana hai sqlite se"
    ],
    "Admin Portal": [
        "mujhe sab manage karne ke liye ek panel",
        "peeche se control karne ka setup",
        "users aur sales track karne ke liye screen",
        "dashboard bana dena data dekhne ke liye",
        "ek CMS portal jaha se update ho sake"
    ]
}

def generate_dataset():
    dataset = []
    
    # Generate exactly 1250 prompts (125 per class * 10 classes)
    for expected_class, core_list in CORES.items():
        for core in core_list:
            for prefix in PREFIXES:
                for suffix in SUFFIXES:
                    # Construct sentence
                    parts = []
                    if prefix: parts.append(prefix)
                    parts.append(core)
                    if suffix: parts.append(suffix)
                    
                    prompt = " ".join(parts).strip()
                    dataset.append({
                        "prompt": prompt,
                        "expected": expected_class
                    })
                    
    # Shuffle the dataset
    random.shuffle(dataset)
    
    # Save to JSON
    with open('benchmark_v2_1250.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Generated {len(dataset)} prompts across {len(CORES)} classes.")
    print("Dataset saved to benchmark_v2_1250.json")

if __name__ == "__main__":
    generate_dataset()
