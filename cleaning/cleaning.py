# mccole:setup
import random
from datetime import datetime, timedelta

import polars as pl

random.seed(42)

KINDS = ["storm", "flood", "power-outage", "fire"]
STATUSES = ["reported", "assigned", "resolved"]
SEVERITIES = ["low", "medium", "high"]
LAT_RANGE = (40.0, 42.0)
# mccole:/setup

# mccole:generate
def random_timestamp():
    start = datetime(2024, 6, 1, 0, 0, 0)
    return start + timedelta(minutes=random.randint(0, 7 * 24 * 60))

rows = []
for i in range(40):
    rows.append({
        "id": i + 1,
        "timestamp": random_timestamp(),
        "latitude": round(random.uniform(*LAT_RANGE), 4),
        "longitude": round(random.uniform(-76.0, -73.0), 4),
        "kind": random.choice(KINDS),
        "severity": random.choice(SEVERITIES),
        "status": random.choice(STATUSES),
        "responder_id": random.randint(100, 199),
    })
# mccole:/generate

# mccole:inject_dirt
rows[5]["kind"] = "Flood"       # wrong capitalization
rows[7]["kind"] = "flooding"    # synonym, not a controlled label
rows[12]["status"] = "Resolved" # wrong capitalization
rows[18]["status"] = "closed"   # synonym, not a controlled label
rows[20]["severity"] = None     # missing value
rows[24]["severity"] = None     # another missing value
rows[33]["latitude"] = 999.0    # out of range
rows[35]["latitude"] = None     # missing value

rows.append(dict(rows[3]))      # the same id logged twice

reentered = dict(rows[11])      # the same event re-keyed with a fresh id
reentered["id"] = 1000
rows.append(reentered)

raw = pl.DataFrame(rows)
print(raw.head())
# mccole:/inject_dirt

# mccole:profile
print(raw.shape)

print(raw.schema)

print(raw.null_count())

print(raw.select(
    pl.col("latitude").min().alias("lat_min"),
    pl.col("latitude").max().alias("lat_max"),
))

print(raw.group_by("kind").agg(pl.len().alias("count")))

print(raw.group_by("status").agg(pl.len().alias("count")))
# mccole:/profile

# mccole:dedup
dup_keys = ["kind", "latitude", "longitude", "timestamp"]
n_raw = raw.height
deduped = raw.unique(subset=dup_keys, keep="first")
print("removed", n_raw - deduped.height, "duplicates;", deduped.height, "rows remain")
# mccole:/dedup

# mccole:normalize
KIND_FIXES = {"flooding": "flood"}
STATUS_FIXES = {"closed": "resolved"}

def fix_labels(col, fixes):
    lowered = pl.col(col).str.to_lowercase()
    for wrong, right in fixes.items():
        lowered = pl.when(lowered == wrong).then(pl.lit(right)).otherwise(lowered)
    return lowered

clean = deduped.with_columns(
    fix_labels("kind", KIND_FIXES).alias("kind"),
    fix_labels("status", STATUS_FIXES).alias("status"),
)

print(clean.group_by("kind").agg(pl.len().alias("count")))
print(clean.group_by("status").agg(pl.len().alias("count")))
# mccole:/normalize

# mccole:fill_missing
clean = clean.with_columns(pl.col("severity").fill_null("unknown").alias("severity"))
# mccole:/fill_missing

# mccole:validate
n_before_validate = clean.height
clean = clean.filter(
    pl.col("latitude").is_not_null()
    & pl.col("latitude").is_between(*LAT_RANGE)
    & pl.col("kind").is_in(KINDS)
    & pl.col("status").is_in(STATUSES)
    & pl.col("severity").is_in(SEVERITIES + ["unknown"])
)

print("dropped", n_before_validate - clean.height, "unplaceable rows")
print(clean.null_count())
# mccole:/validate

# mccole:report
report = {
    "rows": {"before": n_raw, "after": clean.height},
    "duplicates_removed": n_raw - deduped.height,
    "rows_dropped_bad_location": n_before_validate - clean.height,
    "missing_severity_filled": raw["severity"].null_count(),
}
print(report)
# mccole:/report
