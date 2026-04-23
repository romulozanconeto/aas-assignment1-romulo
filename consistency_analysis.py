import json
import statistics
from collections import defaultdict

with open('results/metrics/all_metrics_v2.json', 'r') as f:
    metrics = json.load(f)

by_case = defaultdict(list)
for m in metrics:
    by_case[m["case_id"]].append(m["f1"])

print("=== Consistency by test case ===\n")
print(f"{'Case':<20} {'Average F1':<12} {'Deviation':<15} {'Total variation':<15}")
print("-" * 65)

for case_id in sorted(by_case.keys()):
    values = by_case[case_id]
    avg = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0
    total_variation = "Yes" if min(values) == 0 and max(values) > 0 else "No"
    print(f"{case_id:<20} {avg:<12.3f} {stdev:<15.3f} {total_variation:<15}")
