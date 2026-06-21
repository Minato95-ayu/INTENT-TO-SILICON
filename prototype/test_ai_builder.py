import os
import sys

# Mock get_gemini_key
def mock_get_key():
    return "mock"

# Mock call_gemini
def mock_call_gemini(prompt, system_instruction=None, json_mode=False):
    if json_mode:
        return '''{
            "project_name": "BlogApp",
            "entities": ["Post", "User"],
            "routes": ["/", "/dashboard"],
            "auth": true,
            "database": "sqlite"
        }'''
    else:
        return "INTENT_LOCKED"

# Inject mocks
import ai_builder
ai_builder.get_gemini_key = mock_get_key
ai_builder.call_gemini = mock_call_gemini

# Run generator only up to step 4
transcript = ai_builder.run_clarification_engine("test")
arch = ai_builder.generate_architecture(transcript)
ai_builder.generate_aayu_project(arch)

print("Generated successfully!")
