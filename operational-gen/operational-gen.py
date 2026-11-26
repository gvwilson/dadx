# mccole:imports
import math
import random
from datetime import date, timedelta

import altair as alt
import polars as pl

SEED = 20261108
random.seed(SEED)
# mccole:/imports

# mccole:river_constants
N_YEARS = 2
N_DAYS = N_YEARS * 365    # daily readings over two years
PERIOD = 365              # days per year: the seasonal cycle
BASE = 3.0                # metres: typical river level
SLOPE = 0.001             # metres per day: a slow, steady rise
AMPLITUDE = 0.6           # metres: the yearly swing
PHASE = 2.2               # radians: shifts the peak to the calendar
NOISE = 0.12              # metres: day-to-day jitter

FLOOD_DAY = 500           # the day we inject the flood
FLOOD_JUMP = 3.0          # metres: the brief excursion
# mccole:/river_constants

# mccole:make_river_levels
def make_river_levels(n):
    start = date(2024, 1, 1)
    rows = []
    for t in range(n):
        seasonal = AMPLITUDE * math.sin(2 * math.pi * t / PERIOD + PHASE)
        noise = random.gauss(0.0, NOISE)
        level = BASE + SLOPE * t + seasonal + noise
        flood = t == FLOOD_DAY
        if flood:
            level += FLOOD_JUMP
        rows.append({
            "timestamp": (start + timedelta(days=t)).isoformat(),
            "station_id": 1,
            "river_level": round(level, 3),
            "anomaly": flood,
        })
    return rows

readings = pl.DataFrame(make_river_levels(N_DAYS))
readings.head()
# mccole:/make_river_levels

# mccole:plot_river
base = alt.Chart(readings).encode(x="timestamp:T")
line = base.mark_line().encode(y="river_level:Q")
marks = base.mark_point(color="red", size=60).encode(
    y="river_level:Q"
).transform_filter("datum.anomaly")
chart = (line + marks).properties(width=600, height=220)
chart.save("river-levels.json")
# mccole:/plot_river

# mccole:make_environment
T_BASE = 15.0             # degrees C: mean annual temperature
T_AMPLITUDE = 10.0        # degrees C: summer peak, winter trough
T_NOISE = 1.2             # degrees C: day-to-day jitter
P_BASE = 40.0             # ppm: typical pollution level
P_NOISE = 3.0             # ppm: day-to-day jitter
SPIKE_DAY = 500           # the day we inject the pollution spike
SPIKE_JUMP = 120.0        # ppm: the brief excursion

def make_environment(n):
    start = date(2024, 1, 1)
    rows = []
    for t in range(n):
        seasonal = T_AMPLITUDE * math.sin(2 * math.pi * t / PERIOD + PHASE)
        temperature = T_BASE + seasonal + random.gauss(0.0, T_NOISE)
        pollution = P_BASE + random.gauss(0.0, P_NOISE)
        spike = t == SPIKE_DAY
        if spike:
            pollution += SPIKE_JUMP
        rows.append({
            "date": (start + timedelta(days=t)).isoformat(),
            "site_id": 1,
            "temperature_c": round(temperature, 2),
            "pollution_ppm": round(pollution, 2),
            "anomaly": spike,
        })
    return rows

environment = pl.DataFrame(make_environment(N_DAYS))
environment.head()
# mccole:/make_environment

# mccole:plot_pollution
base = alt.Chart(environment).encode(x="date:T")
line = base.mark_line().encode(y="pollution_ppm:Q")
marks = base.mark_point(color="red", size=60).encode(
    y="pollution_ppm:Q"
).transform_filter("datum.anomaly")
chart = (line + marks).properties(width=600, height=220)
chart.save("pollution.json")
# mccole:/plot_pollution
