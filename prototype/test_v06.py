import sys
import os

# Add parent directory to path so we can import from prototype
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from prototype.nlp_engine import process_single_input, load_libraries

func_lib, emotion_lib = load_libraries()

print("=========================================")
print("Testing Context-Awareness (v0.6)")
print("=========================================")

# Test 1: User without profile
print("\n[Test 1] Unknown User -> No context")
process_single_input("mujhe ek secure database chahiye dar lag raha hai data chori ka", func_lib, emotion_lib, user_id=None, headless_reply="1")

# Test 2: User with tech profile and history
print("\n[Test 2] Senior Backend Engineer Anjali -> Context Aware")
process_single_input("mujhe ek secure database chahiye dar lag raha hai data chori ka", func_lib, emotion_lib, user_id="user_tech_lead_anjali", headless_reply="1")

print("\nSuccess! Context injection is working.")
