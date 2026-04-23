import json
import os
from pathlib import Path
from llm_runner import run_batch
from evaluation_engine import evaluate_all_responses

def load_cases(dataset_path):
    with open(dataset_path, "r") as f:
        data = json.load(f)
    return data["cases"]

def load_prompt(prompt_path):
    with open(prompt_path, "r") as f:
        return f.read()

def load_ground_truth(dataset_path):
    with open(dataset_path, "r") as f:
        data = json.load(f)
    gt = {}
    for case in data["cases"]:
        gt[case["id"]] = case["ground_truth_vuln"]
    return gt

def main():
    base_dir = Path(__file__).parent.parent
    dataset_path = base_dir / "dataset" / "cases.json"
    prompts_dir = base_dir / "prompts"
    results_raw_dir = base_dir / "results" / "raw"
    results_metrics_dir = base_dir / "results" / "metrics"
    
    print("Loading cases...")
    cases = load_cases(dataset_path)
    print(f"Loaded {len(cases)} test cases")
    
    print("Loading prompts...")
    simple_prompt = load_prompt(prompts_dir / "simple_prompt.txt")
    structured_prompt = load_prompt(prompts_dir / "structured_prompt.txt")
    
    print("\n=== Running with SIMPLE prompt ===")
    run_batch(cases, "simple", simple_prompt, results_raw_dir)
    
    print("\n=== Running with STRUCTURED prompt ===")
    run_batch(cases, "structured", structured_prompt, results_raw_dir)
    
    print("\n=== Evaluating results ===")
    ground_truth = load_ground_truth(dataset_path)
    metrics_output = results_metrics_dir / "all_metrics.json"
    evaluate_all_responses(results_raw_dir, ground_truth, metrics_output)
    
    print(f"\nEvaluation complete. Results saved to {metrics_output}")

if __name__ == "__main__":
    main()
