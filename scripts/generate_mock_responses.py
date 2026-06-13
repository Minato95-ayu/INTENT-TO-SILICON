import csv
import random
import os

def generate_mock_responses():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_file = os.path.join(base_dir, 'data', 'human_eval_template.csv')
    
    if not os.path.exists(template_file):
        print("Template not found.")
        return
        
    responses = []
    
    categories = [
        "payment_anxiety",
        "otp_failure",
        "navigation_confusion",
        "performance_frustration",
        "trust_deficit",
        "support_frustration"
    ]
    
    with open(template_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            phrase = row['phrase']
            actual = row['actual_category']
            
            human_label = actual
            
            if actual == "mixed":
                # For mixed, humans will guess randomly from the available categories
                # Let's try to map some based on keywords for realism
                if "payment" in phrase or "paise" in phrase or "500" in phrase:
                    human_label = "payment_anxiety"
                elif "otp" in phrase or "login" in phrase:
                    human_label = "otp_failure"
                elif "slow" in phrase or "crash" in phrase or "loading" in phrase:
                    human_label = "performance_frustration"
                elif "setting" in phrase or "click" in phrase or "menu" in phrase:
                    human_label = "navigation_confusion"
                else:
                    human_label = random.choice(categories)
            else:
                # 15% chance of human disagreement/error
                if random.random() < 0.15:
                    human_label = random.choice(categories)
                    
            responses.append([phrase, actual, human_label])
            
    output_path = os.path.join(base_dir, 'data', 'mock_human_responses.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['phrase', 'actual_category', 'human_label'])
        writer.writerows(responses)
        
    print(f"Generated mock responses at {output_path}")

if __name__ == "__main__":
    generate_mock_responses()
