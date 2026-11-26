# mccole:import
import random
import statistics
from datetime import datetime, timedelta

import altair as alt
import polars as pl

random.seed(7)
# mccole:/import

# mccole:generate
N = 200                  # hourly readings, a bit over a week
BASELINE = 2.0           # meters: the gauge's usual level
NOISE = 0.1              # meters: hour-to-hour jitter
start = datetime(2024, 6, 1, 0, 0, 0)

levels = []
for i in range(N):
    level = BASELINE + random.gauss(0.0, NOISE)
    if 100 <= i <= 103:  # a short flood spike
        level += 4.0
    levels.append(round(level, 3))

df = pl.DataFrame({
    "timestamp": [start + timedelta(hours=i) for i in range(N)],
    "level": levels,
})
print(df.head())
# mccole:/generate

# mccole:z_scores
mean = statistics.fmean(df["level"])
sd = statistics.stdev(df["level"])
print(mean, sd)
# mccole:/z_scores

# mccole:flag
THRESHOLD = 3.0

df = df.with_columns(
    ((pl.col("level") - mean) / sd).alias("z"),
)
df = df.with_columns(
    (pl.col("z").abs() > THRESHOLD).alias("flag"),
)
print(df.filter(pl.col("flag")))
# mccole:/flag

# mccole:plot
base = alt.Chart(df).encode(x="timestamp:T")
line = base.mark_line().encode(y="level:Q")
marks = base.mark_point(color="red", size=70).encode(y="level:Q").transform_filter("datum.flag")
chart = (line + marks).properties(width=600, height=200)
chart.save("anomaly.json")
# mccole:/plot

# mccole:rolling
WINDOW = 12  # hours: a moving baseline

df = df.with_columns(
    pl.col("level").rolling_mean(window_size=WINDOW).alias("roll_mean"),
    pl.col("level").rolling_std(window_size=WINDOW).alias("roll_std"),
)
df = df.with_columns(
    ((pl.col("level") - pl.col("roll_mean")) / pl.col("roll_std")).alias("roll_z"),
)
df = df.with_columns(
    (pl.col("roll_z").abs() > THRESHOLD).alias("roll_flag"),
)
print(df.filter(pl.col("roll_flag")))
# mccole:/rolling
