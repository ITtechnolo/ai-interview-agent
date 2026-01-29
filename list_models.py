import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.environ.get("GOOGLE_API_KEY")
if not key:
    print("No API key found in .env")
else:
    try:
        genai.configure(api_key=key)
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
