# start snippet setup
import random
import statistics

import polars as pl

random.seed(20241108)
# end snippet setup

# start snippet generate
n = 200
mean_a, mean_b = 120.0, 110.0
sd = 25.0

times_a = [random.gauss(mean_a, sd) for _ in range(n)]
times_b = [random.gauss(mean_b, sd) for _ in range(n)]

print(f"A: {statistics.mean(times_a):.1f}s  B: {statistics.mean(times_b):.1f}s")
# end snippet generate

# start snippet dataframe
rows = [("A", t) for t in times_a] + [("B", t) for t in times_b]
df = pl.DataFrame(rows, schema=["variant", "response_time"], orient="row")

print(df.group_by("variant").len())
print(df.head(5))
# end snippet dataframe

# start snippet observed_difference
observed = statistics.mean(times_a) - statistics.mean(times_b)
print(f"observed A - B = {observed:.1f}s")
# end snippet observed_difference

# start snippet permutation_test
all_times = times_a + times_b
num_shuffles = 10_000
extreme = 0

for _ in range(num_shuffles):
    random.shuffle(all_times)
    left = statistics.mean(all_times[:n])
    right = statistics.mean(all_times[n:])
    if abs(left - right) >= abs(observed):
        extreme += 1

p_value = extreme / num_shuffles
print(f"permutation p-value = {p_value:.4f}")
# end snippet permutation_test

# start snippet bootstrap
num_boot = 10_000
boot_diffs = []

for _ in range(num_boot):
    ra = [random.choice(times_a) for _ in range(n)]
    rb = [random.choice(times_b) for _ in range(n)]
    boot_diffs.append(statistics.mean(ra) - statistics.mean(rb))

boot_diffs.sort()
lower = boot_diffs[int(0.025 * num_boot)]
upper = boot_diffs[int(0.975 * num_boot)]
print(f"bootstrap 95% CI for A - B = [{lower:.1f}, {upper:.1f}]s")
# end snippet bootstrap
