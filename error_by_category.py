import json
from collections import defaultdict

with open('results/metrics/all_metrics_v2.json', 'r') as f:
    metrics = json.load(f)

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

error_types = ["correct", "partial_omission", "commission", "mixed"]
by_category_error = {cat: {et: 0 for et in error_types} for cat in set(category_map.values())}

for m in metrics:
    cat = category_map.get(m["case_id"])
    if cat:
        by_category_error[cat][m["error_type"]] += 1

print("=== Distribution of errors by category ===\n")
print(f"{'Category':<10} {'Correct':<10} {'Partial omission':<15} {'Commission':<10} {'Mixed':<10} {'Total':<10}")
print("-" * 70)

for cat in sorted(by_category_error.keys()):
    counts = by_category_error[cat]
    total = sum(counts.values())
    print(f"{cat:<10} {counts['correct']:<10} {counts['partial_omission']:<15} {counts['commission']:<10} {counts['mixed']:<10} {total:<10}")
