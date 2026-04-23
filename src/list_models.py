import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("Listing all available models...")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json()
    print(f"\nFound {len(models.get('models', []))} models:\n")
    for model in models.get("models", []):
        name = model.get("name", "").replace("models/", "")
        supported_methods = model.get("supportedGenerationMethods", [])
        if "generateContent" in supported_methods:
            print(f"  ✓ {name} (supports generateContent)")
        else:
            print(f"  ✗ {name} (does not support generateContent)")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
