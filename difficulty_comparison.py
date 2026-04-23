import json
from collections import defaultdict

with open('results/metrics/all_metrics_v2.json', 'r') as f:
    metrics = json.load(f)

# Mapping each case to your specific situation.
difficulty_map = {
    "A01_SIMPLE_001": "simple", "A01_COMPLEX_001": "complex",
    "A02_SIMPLE_001": "simple", "A02_COMPLEX_001": "complex",
    "A03_SIMPLE_001": "simple", "A03_COMPLEX_001": "complex",
    "A04_SIMPLE_001": "simple", "A04_COMPLEX_001": "complex",
    "A05_SIMPLE_001": "simple", "A05_COMPLEX_001": "complex",
    "A06_SIMPLE_001": "simple", "A06_COMPLEX_001": "complex",
    "A07_SIMPLE_001": "simple", "A07_COMPLEX_001": "complex",
    "A08_SIMPLE_001": "simple", "A08_COMPLEX_001": "complex",
    "A09_SIMPLE_001": "simple", "A09_COMPLEX_001": "complex",
    "A10_SIMPLE_001": "simple", "A10_COMPLEX_001": "complex"
}

simple_f1 = []
complex_f1 = []

for m in metrics:
    difficulty = difficulty_map.get(m["case_id"])
    if difficulty == "simple":
        simple_f1.append(m["f1"])
    elif difficulty == "complex":
        complex_f1.append(m["f1"])

avg_simple = sum(simple_f1) / len(simple_f1) if simple_f1 else 0
avg_complex = sum(complex_f1) / len(complex_f1) if complex_f1 else 0

print("=== Comparison between simple and structured case ===\n")
print(f"Simple Case: {len(simple_f1)} executions")
print(f"  Average F1-score: {avg_simple:.3f}")
print(f"Structured Case: {len(complex_f1)} executions")
print(f"  Average F1-score: {avg_complex:.3f}")
print(f"\nDifference (simple - structured): {avg_simple - avg_complex:+.3f}")
