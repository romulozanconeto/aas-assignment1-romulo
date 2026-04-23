import json
from pathlib import Path
from collections import defaultdict

def generate_report(metrics_file):
    with open(metrics_file, "r") as f:
        metrics = json.load(f)
    
    by_case = defaultdict(lambda: {"simple": [], "structured": []})
    for m in metrics:
        by_case[m["case_id"]][m["prompt_strategy"]].append(m["f1"])
    
    print("=== F1-score by case and strategy ===\n")
    print(f"{'Case ID':<15} {'Simple (avg)':<15} {'Structured (avg)':<15} {'Improvement':<12}")
    print("-" * 60)
    
    for case_id, values in sorted(by_case.items()):
        simple_avg = sum(values["simple"]) / len(values["simple"]) if values["simple"] else 0
        structured_avg = sum(values["structured"]) / len(values["structured"]) if values["structured"] else 0
        improvement = structured_avg - simple_avg
        print(f"{case_id:<15} {simple_avg:<15.3f} {structured_avg:<15.3f} {improvement:+.3f}")
    
    print("\n=== Error types distribution ===\n")
    error_counts = defaultdict(int)
    for m in metrics:
        error_counts[m["error_type"]] += 1
    
    for error_type, count in sorted(error_counts.items()):
        print(f"{error_type}: {count}")
    
    print("\n=== F1-score by category ===\n")
    category_map = {
        "A01_SIMPLE_001": "A01", "A01_COMPLEX_001": "A01",
        "A02_SIMPLE_001": "A02", "A02_COMPLEX_001": "A02",
        "A03_SIMPLE_001": "A03", "A03_COMPLEX_001": "A03",
        "A04_SIMPLE_001": "A04", "A04_COMPLEX_001": "A04",
        "A05_SIMPLE_001": "A05", "A05_COMPLEX_001": "A05",
        "A06_SIMPLE_001": "A06", "A06_COMPLEX_001": "A06",
        "A07_SIMPLE_001": "A07", "A07_COMPLEX_001": "A07",
        "A08_SIMPLE_001": "A08", "A08_COMPLEX_001": "A08",
        "A09_SIMPLE_001": "A09", "A09_COMPLEX_001": "A09",
        "A10_SIMPLE_001": "A10", "A10_COMPLEX_001": "A10"
    }
    
    by_category = defaultdict(lambda: {"simple": [], "structured": []})
    for m in metrics:
        cat = category_map.get(m["case_id"], "UNKNOWN")
        by_category[cat][m["prompt_strategy"]].append(m["f1"])
    
    print(f"{'Category':<10} {'Simple (avg)':<15} {'Structured (avg)':<15} {'Difference':<12}")
    print("-" * 55)
    
    for cat in sorted(by_category.keys()):
        simple_avg = sum(by_category[cat]["simple"]) / len(by_category[cat]["simple"]) if by_category[cat]["simple"] else 0
        structured_avg = sum(by_category[cat]["structured"]) / len(by_category[cat]["structured"]) if by_category[cat]["structured"] else 0
        diff = structured_avg - simple_avg
        print(f"{cat:<10} {simple_avg:<15.3f} {structured_avg:<15.3f} {diff:+.3f}")

if __name__ == "__main__":
    metrics_path = Path("results/metrics/all_metrics.json")
    if metrics_path.exists():
        generate_report(metrics_path)
    else:
        print("Metrics file not found. Run main.py first.")
