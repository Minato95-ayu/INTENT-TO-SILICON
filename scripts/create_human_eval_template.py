import csv
import random
import os

def create_template():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    corpus_file = os.path.join(base_dir, 'data', 'corpus_v1', 'payment_anxiety.csv')
    
    if not os.path.exists(corpus_file):
        print("Corpus file not found.")
        return
        
    phrases = []
    with open(corpus_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            phrases.append(row['phrase'])
            
    # Select 50 random phrases
    selected = random.sample(phrases, min(50, len(phrases)))
    
    output_path = os.path.join(base_dir, 'data', 'human_eval_template.csv')
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['phrase', 'correct_label'])
        for p in selected:
            writer.writerow([p, ''])
            
    print(f"Created template at {output_path} with {len(selected)} phrases.")

if __name__ == "__main__":
    create_template()
