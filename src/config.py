import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

TEMPERATURE = 1.0
TOP_P = 0.95
MAX_OUTPUT_TOKENS = 8192

EXECUTIONS_PER_CASE = 5
DELAY_BETWEEN_REQUESTS = 5
