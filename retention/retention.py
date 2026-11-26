# mccole:import
import polars as pl
import altair as alt
import random

random.seed(12345)
# mccole:/import

# mccole:helpers
START_YEAR = 2024

def month_index(ym):
    """'2024-03' -> an integer month number (0 = 2024-01)."""
    year, month = ym.split("-")
    return (int(year) - START_YEAR) * 12 + int(month) - 1

def month_label(idx):
    """An integer month number -> '2024-03'."""
    return f"{START_YEAR + idx // 12:04d}-{idx % 12 + 1:02d}"
# mccole:/helpers

# mccole:generate
roles = ["medic", "logistics", "search", "comms"]
names = ["Aisha", "Ben", "Cara", "Dmitri", "Elena", "Farid",
         "Grace", "Hiro", "Ines", "Jules", "Keiko", "Liam"]

responders = []
incidents = []
rid = 0

for cohort in range(6):                     # six first-response months
    for _ in range(random.randint(6, 10)):  # volunteers per cohort
        rid += 1
        name = random.choice(names)
        role = random.choice(roles)
        joined = max(0, cohort - random.randint(0, 2))
        responders.append((rid, name, month_label(joined), role))
        lifetime = max(1, round(random.gauss(4, 1.5)))
        for k in range(lifetime):           # months since first response
            for _ in range(random.randint(1, 3)):
                incidents.append((len(incidents) + 1, month_label(cohort + k), rid))
# mccole:/generate

# mccole:tables
responders = pl.DataFrame(
    responders, schema=["id", "name", "joined", "role"], orient="row"
)
incidents = pl.DataFrame(
    incidents, schema=["id", "timestamp", "responder_id"], orient="row"
)

print(responders.head())
print(incidents.head())
# mccole:/tables

# mccole:month_index
incidents = incidents.with_columns(
    month_idx=pl.col("timestamp").map_elements(month_index, return_dtype=pl.Int64)
)
# mccole:/month_index

# mccole:join
responses = incidents.join(
    responders.select("id", "name", "joined", "role"),
    left_on="responder_id", right_on="id",
)

cohorts = (
    responses.group_by("responder_id")
    .agg(pl.col("month_idx").min().alias("cohort_idx"))
)
# mccole:/join

# mccole:active
active = (
    responses.join(cohorts, on="responder_id")
    .with_columns(period=pl.col("month_idx") - pl.col("cohort_idx"))
)
# mccole:/active

# mccole:retention
retention = (
    active.group_by("cohort_idx", "period")
    .agg(pl.col("responder_id").n_unique().alias("active"))
    .sort(["cohort_idx", "period"])
)

print(retention.head())
# mccole:/retention

# mccole:check
sizes = cohorts.group_by("cohort_idx").len().sort("cohort_idx")
first = (
    retention.filter(pl.col("period") == 0)
    .select(["cohort_idx", "active"])
    .sort("cohort_idx")
)
assert (sizes["len"] == first["active"]).all()
# mccole:/check

# mccole:rate
rate = (
    retention.join(sizes.rename({"len": "size"}), on="cohort_idx")
    .with_columns(rate=pl.col("active") / pl.col("size"))
)

print(rate.head())
# mccole:/rate

# mccole:plot
plot = retention.with_columns(
    cohort=pl.col("cohort_idx").map_elements(month_label, return_dtype=pl.String),
    months_since=pl.col("period"),
)

chart = (
    alt.Chart(plot).mark_rect().encode(
        x=alt.X("months_since:O", title="months since first response"),
        y=alt.Y("cohort:N", title="cohort (first-response month)"),
        color=alt.Color("active:Q", scale=alt.Scale(scheme="greens")),
        tooltip=["cohort", "months_since", "active"],
    ).properties(title="Volunteer retention by cohort")
)
chart.save("retention.json")
# mccole:/plot
