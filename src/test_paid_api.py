import os
from dotenv import load_dotenv
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

payload = {
    "contents": [{
        "parts": [{"text": "Reply with only the word: OK"}]
    }],
    "generationConfig": {
        "temperature": 1.0,
        "maxOutputTokens": 10
    }
}

url = f"{API_URL}?key={GEMINI_API_KEY}"
print(f"Testing URL: {API_URL}")
response = requests.post(url, json=payload, timeout=30)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("API working with gemini-1.5-flash")
    result = response.json()
    print(result["candidates"][0]["content"]["parts"][0]["text"])
else:
    print(f"Error: {response.text}")
