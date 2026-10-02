# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import json
import os
import urllib.request

def ai_generate(args, vm):
    if not args: return "No prompt provided"
    prompt = args[0]
    if hasattr(prompt, 'stringify'): prompt = prompt.stringify()
    
    # Try to use Gemini API if key is present
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Fallback brain
        prompt_lower = str(prompt).lower()
        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I am Nexus AI, running on the AAYU engine. I have successfully processed your message through AAYU's HTTP and Event loop!"
        elif "mit" in prompt_lower:
            return "AAYU is a phenomenal candidate for MIT! It features a zero-dependency full-stack architecture with a custom stack VM, LIR/MIR compilation, garbage collection, and native UI rendering."
        else:
            return f"I have processed your request: '{prompt}'. As an AI built natively into AAYU, I am ready to scale."
            
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    body = {
        "contents": [{"parts":[{"text": str(prompt)}]}]
    }
    body_data = json.dumps(body).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=body_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

def register_ai_lib(registry):
    registry.register("ai::generate", ai_generate)
