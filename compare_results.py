import json

with open('results/metrics/all_metrics.json', 'r') as f:
    old_metrics = json.load(f)

with open('results/metrics/all_metrics_v2.json', 'r') as f:
    new_metrics = json.load(f)

old_f1 = sum(m['f1'] for m in old_metrics) / len(old_metrics)
new_f1 = sum(m['f1'] for m in new_metrics) / len(new_metrics)

print(f"Average F1-score (old version): {old_f1:.3f}")
print(f"Average F1-score (new version): {new_f1:.3f}")
print(f"Difference between 2 versions: {new_f1 - old_f1:+.3f}")

# Error type count in the new version
from collections import Counter
error_counts = Counter(m['error_type'] for m in new_metrics)
print(f"\nError distribution (new version):")
for error_type, count in sorted(error_counts.items()):
    print(f"  {error_type}: {count}")
