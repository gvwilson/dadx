# start snippet make_sample
import random
from datetime import datetime, timedelta

random.seed(20261108)

KINDS = ["storm", "flood", "power-outage", "fire"]
STATUSES = ["reported", "triaged", "dispatched", "resolved"]
BASE = datetime(2024, 6, 1, 0, 0, 0)

def make_incidents(n, n_responders=20):
    rows = []
    for i in range(1, n + 1):
        when = BASE + timedelta(
            days=random.randint(0, 60),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        rows.append({
            "id": i,
            "timestamp": when.isoformat(),
            "latitude": round(random.uniform(-40.0, -30.0), 4),
            "longitude": round(random.uniform(140.0, 150.0), 4),
            "kind": random.choice(KINDS),
            "severity": random.randint(1, 5),
            "status": random.choice(STATUSES),
            "responder_id": random.randint(1, n_responders),
        })
    return rows
# end snippet make_sample

# start snippet ingest
import polars as pl

pl.DataFrame(make_incidents(120)).write_csv("incidents.csv")
raw = pl.read_csv("incidents.csv")
print(raw.head())
# end snippet ingest

# start snippet clean_profile
print(raw.schema)
print(raw.null_count())
# end snippet clean_profile

# start snippet clean_parse
cleaned = raw.with_columns(
    pl.col("timestamp").str.to_datetime(format="%Y-%m-%dT%H:%M:%S")
)
print(cleaned.schema)
# end snippet clean_parse

# start snippet explore_select
cols = cleaned.select(["id", "kind", "severity", "status"])
print(cols.head())
# end snippet explore_select

# start snippet explore_filter
high = cleaned.filter(pl.col("severity") >= 4)
print(high.shape)
# end snippet explore_filter

# start snippet summarize_kind
by_kind = cleaned.group_by("kind").len().sort("len", descending=True)
print(by_kind)
# end snippet summarize_kind

# start snippet summarize_severity
by_severity = cleaned.group_by("severity").len().sort("severity")
print(by_severity)
# end snippet summarize_severity

# start snippet reshape
matrix = (
    cleaned.group_by("kind", "severity")
    .len()
    .pivot(on="severity", index="kind", values="len", sort_columns=True)
)
print(matrix)
# end snippet reshape

# start snippet plot
import altair as alt

chart = (
    alt.Chart(by_kind)
    .mark_bar()
    .encode(
        x=alt.X("kind:N", sort="-y", title="kind"),
        y=alt.Y("len:Q", title="incidents"),
    )
    .properties(title="Incidents per kind")
)
chart.save("chart.json")
# end snippet plot

# start snippet check
assert by_kind["len"].sum() == cleaned.height
assert set(by_kind["kind"]) == set(KINDS)
# end snippet check
