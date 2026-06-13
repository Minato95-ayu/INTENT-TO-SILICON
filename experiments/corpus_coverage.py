import os
import csv
import sys
import glob

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'prototype'))

from nlp_engine import load_libraries, process_single_input

def test_corpus_coverage():
    func_lib, emotion_lib = load_libraries()
    
    corpus_dir = os.path.join(base_dir, 'data', 'corpus_v1')
    if not os.path.exists(corpus_dir):
        print(f"Directory not found: {corpus_dir}")
        return
        
    csv_files = glob.glob(os.path.join(corpus_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found in data/corpus_v1/")
        return
        
    total_phrases = 0
    matched = 0
    oov = 0
    
    print("==================================================")
    print(" CORPUS COVERAGE BENCHMARK (v1)")
    print("==================================================")
    
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        file_total = 0
        file_matched = 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                phrase = row['phrase']
                file_total += 1
                total_phrases += 1
                
                # Mock headless reply since we only care about initial coverage, not deep disambiguation here
                metrics = process_single_input(phrase, func_lib, emotion_lib, headless_reply="1")
                
                if metrics["status"] == "fail_hard":
                    oov += 1
                else:
                    matched += 1
                    file_matched += 1
                    
        print(f"File: {file_name}")
        print(f"  Phrases: {file_total}")
        print(f"  Matched: {file_matched}")
        print(f"  OOV: {file_total - file_matched}")
        if file_total > 0:
            print(f"  Coverage: {(file_matched/file_total)*100:.1f}%\n")
        
    print("==================================================")
    print(" OVERALL RESULTS")
    print("==================================================")
    print(f"Total phrases: {total_phrases}")
    print(f"Matched: {matched}")
    print(f"OOV: {oov}")
    if total_phrases > 0:
        coverage = (matched / total_phrases) * 100
        print(f"Coverage: {coverage:.1f}%")
    print("==================================================")

if __name__ == "__main__":
    test_corpus_coverage()
