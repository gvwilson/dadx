# start snippet imports
import math
import random

import altair as alt
import polars as pl

SEED = 20261108
# end snippet imports

# start snippet generate
GROUPS = {
    "storm":        {"code": 0, "severity": 3.0, "spread": 0.5, "n": 60},
    "power-outage": {"code": 1, "severity": 4.5, "spread": 0.5, "n": 50},
    "flood":        {"code": 2, "severity": 6.5, "spread": 0.6, "n": 55},
    "fire":         {"code": 3, "severity": 8.5, "spread": 0.5, "n": 45},
}

def make_incidents(groups):
    random.seed(SEED)
    rows = []
    for kind, spec in groups.items():
        for _ in range(spec["n"]):
            rows.append({
                "kind": kind,
                "kind_code": round(spec["code"] + random.gauss(0.0, 0.15), 3),
                "severity": round(spec["severity"] + random.gauss(0.0, spec["spread"]), 3),
            })
    return pl.DataFrame(rows)

incidents = make_incidents(GROUPS)
print(incidents.head())
# end snippet generate

# start snippet plot_before
chart = alt.Chart(incidents).mark_circle(opacity=0.6).encode(
    x=alt.X("kind_code:Q", title="kind (numeric code)"),
    y=alt.Y("severity:Q", title="severity"),
    color=alt.Color("severity:Q", scale=alt.Scale(scheme="viridis")),
    tooltip=["kind", "severity"],
).properties(width=500, height=300, title="Incidents before clustering")
chart.save("clusters-before.json")
# end snippet plot_before

# start snippet distance
def distance(a, b):
    return math.dist(a, b)
# end snippet distance

# start snippet initialize
def initialize(points, k, seed=SEED):
    rng = random.Random(seed)
    idxs = rng.sample(range(len(points)), k)
    return [points[i] for i in idxs]
# end snippet initialize

# start snippet assign
def assign(points, centroids):
    labels = []
    for p in points:
        dists = [distance(p, c) for c in centroids]
        labels.append(dists.index(min(dists)))
    return labels

def recenter(points, labels, k):
    centroids = []
    for j in range(k):
        members = [p for p, lab in zip(points, labels) if lab == j]
        if not members:
            centroids.append((0.0, 0.0))  # empty cluster: keep a placeholder
            continue
        dims = len(members[0])
        mean = tuple(
            sum(m[d] for m in members) / len(members) for d in range(dims)
        )
        centroids.append(mean)
    return centroids
# end snippet assign

# start snippet kmeans
def kmeans(points, k, seed=SEED, max_iter=100):
    centroids = initialize(points, k, seed)
    labels = None
    for _ in range(max_iter):
        new_labels = assign(points, centroids)
        if new_labels == labels:
            break
        labels = new_labels
        centroids = recenter(points, labels, k)
    return labels, centroids
# end snippet kmeans

# start snippet cluster
points = list(zip(incidents["kind_code"], incidents["severity"]))

K = 4
labels, centroids = kmeans(points, K)

incidents = incidents.with_columns(pl.Series("cluster", labels))
print(incidents.head())
# end snippet cluster

# start snippet plot_clusters
chart = alt.Chart(incidents).mark_circle(opacity=0.6).encode(
    x=alt.X("kind_code:Q", title="kind (numeric code)"),
    y=alt.Y("severity:Q", title="severity"),
    color=alt.Color("cluster:N"),
    tooltip=["kind", "severity", "cluster"],
).properties(width=500, height=300, title="Incidents clustered with k-means")
chart.save("clusters.json")
# end snippet plot_clusters

# start snippet interpret
for cluster in range(K):
    members = incidents.filter(pl.col("cluster") == cluster)
    counts = members["kind"].value_counts().sort("count", descending=True)
    top = counts.row(0, named=True)
    avg = members["severity"].mean()
    print(f"cluster {cluster}: {len(members)} records, "
          f"mostly {top['kind']} ({top['count']}), mean severity {avg:.1f}")
# end snippet interpret

# start snippet validate
_, other = kmeans(points, K, seed=SEED + 1)

for a, b in zip(sorted(centroids), sorted(other)):
    print(f"{tuple(round(x, 2) for x in a)}  vs  {tuple(round(x, 2) for x in b)}")
# end snippet validate

# start snippet sum_squares
def sum_squares(points, labels, centroids):
    total = 0.0
    for p, lab in zip(points, labels):
        c = centroids[lab]
        total += sum((p[d] - c[d]) ** 2 for d in range(len(p)))
    return total
# end snippet sum_squares

# start snippet kmeans_best
def kmeans_best(points, k, starts=8, start_seed=SEED):
    best_score, best_labels, best_centroids = None, None, None
    for s in range(starts):
        labels, centroids = kmeans(points, k, seed=start_seed + s)
        score = sum_squares(points, labels, centroids)
        if best_score is None or score < best_score:
            best_score, best_labels, best_centroids = score, labels, centroids
    return best_labels, best_centroids
# end snippet kmeans_best

# start snippet validate_best
_, best_a = kmeans_best(points, K)
_, best_b = kmeans_best(points, K, start_seed=SEED + 100)

for a, b in zip(sorted(best_a), sorted(best_b)):
    print(f"{tuple(round(x, 2) for x in a)}  vs  {tuple(round(x, 2) for x in b)}")
# end snippet validate_best
