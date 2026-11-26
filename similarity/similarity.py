# mccole:imports
import math
import random

import polars as pl

SEED = 20261108
random.seed(SEED)
# mccole:/imports

# mccole:generate
def make_incidents(n):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "id": i,
            "severity": random.randint(1, 5),
            "latitude": round(random.uniform(-40.0, -30.0), 4),
            "longitude": round(random.uniform(140.0, 150.0), 4),
        })
    return pl.DataFrame(rows)

incidents = make_incidents(12)
print(incidents)
# mccole:/generate

# mccole:distance
def euclidean(a, b):
    return math.dist(a, b)
# mccole:/distance

# mccole:minmax
features = ["severity", "latitude", "longitude"]
print("minimums:", incidents.select(features).min().to_dicts()[0])
print("maximums:", incidents.select(features).max().to_dicts()[0])
# mccole:/minmax

# mccole:scale
def zscore(col):
    return (col - col.mean()) / col.std()

scaled = incidents.with_columns([
    zscore(pl.col(f)).alias(f"{f}_z") for f in features
])
print(scaled.head(3))
# mccole:/scale

# mccole:nearest_neighbors
zcols = [f"{f}_z" for f in features]
query = scaled.row(0, named=True)
q = tuple(query[c] for c in zcols)

distances = [
    euclidean(q, tuple(row[c] for c in zcols))
    for row in scaled.iter_rows(named=True)
]
scaled = scaled.with_columns(pl.Series("distance", distances))

k = 3
nearest = (
    scaled.filter(pl.col("id") != query["id"])
    .sort("distance")
    .head(k)
)
print(nearest.select(["id", "severity", "latitude", "longitude", "distance"]))
# mccole:/nearest_neighbors

# mccole:raw_comparison
q_raw = tuple(query[c] for c in features)
raw_dists = [
    euclidean(q_raw, tuple(row[c] for c in features))
    for row in scaled.iter_rows(named=True)
]
scaled = scaled.with_columns(pl.Series("raw_distance", raw_dists))

raw_nearest = (
    scaled.filter(pl.col("id") != query["id"])
    .sort("raw_distance")
    .head(k)
)
print(raw_nearest.select(["id", "severity", "raw_distance"]))
# mccole:/raw_comparison
