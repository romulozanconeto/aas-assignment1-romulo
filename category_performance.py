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

by_category = defaultdict(list)
for m in metrics:
    cat = category_map.get(m["case_id"])
    if cat:
        by_category[cat].append(m["f1"])

print("=== F1 score by category ===\n")
print(f"{'Category':<10} {'Average F1':<12} {'Minimum':<10} {'Maximum':<10} {'Executions':<10}")
print("-" * 55)

for cat in sorted(by_category.keys()):
    values = by_category[cat]
    avg = sum(values) / len(values)
    print(f"{cat:<10} {avg:<12.3f} {min(values):<10.3f} {max(values):<10.3f} {len(values):<10}")
