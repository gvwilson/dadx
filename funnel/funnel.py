# start snippet setup
import random

import altair as alt
import polars as pl

stages = ["reported", "triaged", "dispatched", "resolved"]
# end snippet setup

# start snippet generate
random.seed(42)
n_incidents = 1000

statuses = []
for _ in range(n_incidents):
    status = "reported"
    if random.random() < 0.75:          # 75% get triaged
        status = "triaged"
        if random.random() < 0.70:      # 70% of those get dispatched
            status = "dispatched"
            if random.random() < 0.60:  # 60% of those get resolved
                status = "resolved"
    statuses.append(status)

incidents = pl.DataFrame({"id": range(1, n_incidents + 1), "status": statuses})
print(incidents.head())
# end snippet generate

# start snippet counts
stage_position = {name: i for i, name in enumerate(stages)}

funnel = (
    incidents.group_by("status")
    .len()
    .with_columns(
        pl.col("status")
        .replace_strict(stage_position, return_dtype=pl.Int64)
        .alias("stage")
    )
    .sort("stage")
    .with_columns(pl.col("len").cum_sum(reverse=True).alias("reached"))
    .select("status", "reached")
)
print(funnel)
# end snippet counts

# start snippet conversion
funnel = funnel.with_columns(
    (pl.col("reached").shift(-1) / pl.col("reached")).alias("conversion"),
    (1 - pl.col("reached").shift(-1) / pl.col("reached")).alias("drop_off"),
)
print(funnel)
# end snippet conversion

# start snippet plot
bars = (
    alt.Chart(funnel)
    .mark_bar()
    .encode(
        x=alt.X("status:N", sort=stages, title="stage"),
        y=alt.Y("reached:Q", title="incidents reached"),
    )
)

labels = (
    alt.Chart(funnel)
    .mark_text(dy=-6)
    .encode(
        x=alt.X("status:N", sort=stages),
        y=alt.Y("reached:Q"),
        text="reached:Q",
    )
)

(bars + labels).properties(title="Incident funnel").save("funnel.json")
# end snippet plot
