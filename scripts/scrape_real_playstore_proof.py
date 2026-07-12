"""
=============================================================================
FILE: scrape_real_playstore_proof.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import pandas as pd
from google_play_scraper import Sort, reviews
import os
import json

def scrape_playstore_reviews():
    print("Scraping real Google Play Reviews for Corpus Proof...")
    
    # Target apps where users face pain points (payment, delivery, performance)
    target_apps = {
        'com.application.zomato': 'Zomato',
        'net.one97.paytm': 'Paytm',
        'com.phonepe.app': 'PhonePe',
        'com.flipkart.android': 'Flipkart'
    }
    
    all_reviews = []
    
    for app_id, app_name in target_apps.items():
        print(f"Fetching reviews for {app_name} ({app_id})...")
        try:
            # Fetch 1-star and 2-star reviews (where pain points exist)
            result, continuation_token = reviews(
                app_id,
                lang='en', # English & Hinglish are usually posted under 'en'
                country='in', # India region for Hinglish
                sort=Sort.NEWEST, # Latest
                count=150, # 150 per app
                filter_score_with=1 # Only 1-star to get complaints/pain points
            )
            
            for r in result:
                all_reviews.append({
                    "id": r["reviewId"],
                    "phrase": r["content"].replace('\n', ' ').strip(),
                    "category": "unknown", # To be human-labeled or LLM-labeled
                    "source": "play_store",
                    "proof_app_name": app_name,
                    "proof_rating": r["score"],
                    "proof_date": str(r["at"])
                })
        except Exception as e:
            print(f"Failed to fetch for {app_name}: {e}")
            
    # Save raw proof dataset
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'data', 'corpus_v1_real.csv')
    
    df = pd.DataFrame(all_reviews)
    if not df.empty:
        # Keep only the first 500
        df = df.head(500)
        df.to_csv(output_path, index=False)
        print(f"\nSUCCESS: Downloaded {len(df)} 100% REAL reviews.")
        print(f"Saved with Review IDs (Verifiable Proof) to: {output_path}")
    else:
        print("No reviews fetched.")

if __name__ == "__main__":
    scrape_playstore_reviews()
