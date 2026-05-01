import random
from collections import defaultdict

with open('shakespeare.txt', 'r') as f:
    text = f.read().lower()

counts = defaultdict(lambda: defaultdict(float))
for i in range(len(text) - 1):
    counts[text[i]][text[i+1]] += 1

for key in counts:
  total_count = sum(counts[key].values())
  for sub_key in counts[key]:
    counts[key][sub_key] = counts[key][sub_key] / total_count

for key in counts:
    total_ratio = sum(counts[key].values())
    assert abs(total_ratio - 1.0) < 1e-9, f"row {key!r} sums to {total_ratio}"

# Chose 't' here, but it could have been any other, or
# could have used random to choose the letter and be sure it would be in the dict
current = output = 't'
for _ in range(500):
    next_chars = counts[current]
    picked_char = random.choices(list(next_chars.keys()), list(next_chars.values()))[0]
    output += picked_char
    current = picked_char

print(output)

