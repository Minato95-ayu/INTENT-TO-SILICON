import pandas as pd
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prototype'))
from nlp_engine import process_single_input, load_libraries

df = pd.read_csv('data/evaluation_dataset.csv')
func_library, emotion_library = load_libraries()

for idx, row in df.iterrows():
    if row['category'] in ['emotional', 'mixed']:
        metrics = process_single_input(row['input'], func_library, emotion_library, headless_reply="1")
        # Check if matched_emotions is empty
        if 'matched_emotions' not in metrics or len(metrics['matched_emotions']) == 0:
            print(f"FAILED EMOTION: {row['input']}")
