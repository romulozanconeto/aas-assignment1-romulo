import json
from pathlib import Path

with open('results/metrics/all_metrics_v2.json', 'r') as f:
    metrics = json.load(f)

# Group by error type
by_error = {
    "commission": [],
    "mixed": [],
    "partial_omission": [],
    "correct": []
}

for m in metrics:
    if m["error_type"] in by_error:
        by_error[m["error_type"]].append(m)

# Find an example for each type.
print("=== Examples of failures for documentation ===\n")

for error_type in ["commission", "mixed", "partial_omission", "correct"]:
    if by_error[error_type]:
        example = by_error[error_type][0]
        case_id = example["case_id"]
        exec_num = example["execution"]
        strategy = example["prompt_strategy"]
        
        # Read the full reply
        json_file = Path(f"results/raw/{case_id}_{strategy}_{exec_num}.json")
        if json_file.exists():
            with open(json_file, 'r') as f:
                raw = json.load(f)
                response_text = ""
                if raw.get("response") and "candidates" in raw["response"]:
                    candidate = raw["response"]["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        response_text = candidate["content"]["parts"][0].get("text", "")[:500]
            
            print(f"\n--- {error_type.upper()} ---")
            print(f"Case: {case_id}, Execution: {exec_num}, Strategy: {strategy}")
            print(f"Reply (first 500 characters)::")
            print(response_text)
            print("\n" + "-" * 50)
