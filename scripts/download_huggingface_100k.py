import os
import pandas as pd
from datasets import load_dataset

def download_huggingface_dataset():
    print("Downloading verified Hugging Face 'app_reviews' dataset for 50K Real Corpus...")
    
    # Load app_reviews dataset from Hugging Face
    try:
        dataset = load_dataset("app_reviews", split="train")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return

    # Convert to Pandas
    df = dataset.to_pandas()
    
    # Select needed columns, we only need the review text. In 'app_reviews', the review text is usually 'review'
    if 'review' in df.columns:
        df = df[['package_name', 'star', 'date', 'review']]
        df = df.rename(columns={'package_name': 'proof_app_name', 'star': 'proof_rating', 'date': 'proof_date', 'review': 'phrase'})
    
    # We only want negative reviews (star <= 2) as these contain the pain points
    df = df[df['proof_rating'] <= 2]
    
    # Take 50,000 rows
    df_50k = df.head(50000).copy()
    
    # Add required columns
    df_50k['category'] = 'unknown'
    df_50k['source'] = 'huggingface_app_reviews'
    df_50k['id'] = range(1, len(df_50k) + 1)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'data', 'corpus_v1_real_50k.csv')
    
    df_50k.to_csv(output_path, index=False)
    
    print(f"SUCCESS: Downloaded {len(df_50k)} REAL reviews.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    download_huggingface_dataset()
