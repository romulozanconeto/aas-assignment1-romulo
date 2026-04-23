import requests
import time
import json
from config import GEMINI_API_KEY, API_URL, TEMPERATURE, TOP_P, MAX_OUTPUT_TOKENS, EXECUTIONS_PER_CASE, DELAY_BETWEEN_REQUESTS

def call_gemini_with_retry(prompt, code, execution_id=0, max_retries=5):
    full_prompt = f"{prompt}\n\n```\n{code}\n```"
    
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "temperature": TEMPERATURE,
            "topP": TOP_P,
            "maxOutputTokens": MAX_OUTPUT_TOKENS
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    url = f"{API_URL}?key={GEMINI_API_KEY}"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 429:
                wait_time = (2 ** attempt) + 1
                print(f"  Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Error in execution {execution_id} after {max_retries} attempts: {e}")
                return None
            wait_time = (2 ** attempt) + 1
            print(f"  Request failed. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}")
            time.sleep(wait_time)
    
    return None

def run_batch(cases, prompt_strategy, prompt_text, output_dir):
    results = []
    total_cases = len(cases)
    
    for case_idx, case in enumerate(cases):
        case_id = case["id"]
        print(f"Processing {case_id} with {prompt_strategy} prompt ({case_idx + 1}/{total_cases})")
        
        for exec_num in range(1, EXECUTIONS_PER_CASE + 1):
            print(f"  Execution {exec_num}/{EXECUTIONS_PER_CASE}")
            
            response = call_gemini_with_retry(prompt_text, case["code"], exec_num)
            
            result = {
                "case_id": case_id,
                "prompt_strategy": prompt_strategy,
                "execution": exec_num,
                "timestamp": time.time(),
                "response": response
            }
            
            output_file = f"{output_dir}/{case_id}_{prompt_strategy}_{exec_num}.json"
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            
            results.append(result)
            
            if exec_num < EXECUTIONS_PER_CASE:
                print(f"  Waiting {DELAY_BETWEEN_REQUESTS} seconds before next execution")
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        if case_idx < total_cases - 1:
            print(f"Waiting 5 seconds before next case")
            time.sleep(5)
    
    return results
