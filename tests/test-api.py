import os

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment variables!")

print("API Key loaded successfully")
