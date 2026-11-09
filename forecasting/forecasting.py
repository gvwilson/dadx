# start snippet setup
import math
import random

import altair as alt
import polars as pl

SEED = 20261108
random.seed(SEED)
# end snippet setup

# start snippet generate
N_YEARS = 6
PERIOD = 12                 # months per year
BASE = 3.0                  # metres
SLOPE = 0.02                # metres per month
AMPLITUDE = 0.8             # metres
PHASE = math.pi / 6
NOISE = 0.15                # metres

def make_river_levels(n):
    rows = []
    for t in range(n):
        seasonal = AMPLITUDE * math.sin(2 * math.pi * t / PERIOD + PHASE)
        noise = random.gauss(0.0, NOISE)
        rows.append({"t": t, "level": BASE + SLOPE * t + seasonal + noise})
    return rows

df = pl.DataFrame(make_river_levels(N_YEARS * PERIOD))
print(df.head())
# end snippet generate

# start snippet split
HOLDOUT = 12

train = df.slice(0, len(df) - HOLDOUT)
test = df.slice(len(df) - HOLDOUT, HOLDOUT)
print(f"train: {len(train)} points, test: {len(test)} points")
# end snippet split

# start snippet baseline
def naive_forecast(train, horizon):
    last_value = train["level"][-1]
    return [last_value] * horizon

naive_pred = naive_forecast(train, HOLDOUT)
print(naive_pred[:4])
# end snippet baseline

# start snippet trend
def fit_trend(t, y):
    t_mean = sum(t) / len(t)
    y_mean = sum(y) / len(y)
    num = sum((ti - t_mean) * (yi - y_mean) for ti, yi in zip(t, y))
    den = sum((ti - t_mean) ** 2 for ti in t)
    slope = num / den
    intercept = y_mean - slope * t_mean
    return intercept, slope
# end snippet trend

# start snippet seasonal
def fit_trend_seasonal(t, y, period):
    intercept, slope = fit_trend(t, y)
    detrended = [yi - (intercept + slope * ti) for ti, yi in zip(t, y)]
    by_month = {m: [] for m in range(period)}
    for ti, d in zip(t, detrended):
        by_month[ti % period].append(d)
    seasonal = {m: sum(v) / len(v) for m, v in by_month.items()}
    fitted = [intercept + slope * ti + seasonal[ti % period] for ti in t]
    residuals = [yi - fi for yi, fi in zip(y, fitted)]
    sigma = (sum(r * r for r in residuals) / len(residuals)) ** 0.5
    return intercept, slope, seasonal, sigma
# end snippet seasonal

# start snippet forecast
def trend_seasonal_forecast(t, y, horizon, period):
    intercept, slope, seasonal, _ = fit_trend_seasonal(t, y, period)
    last_t = t[-1]
    forecast = []
    for k in range(horizon):
        t_k = last_t + k + 1
        forecast.append(intercept + slope * t_k + seasonal[t_k % period])
    return forecast

t_train = train["t"].to_list()
y_train = train["level"].to_list()
trend_pred = trend_seasonal_forecast(t_train, y_train, HOLDOUT, PERIOD)
print(trend_pred[:4])
# end snippet forecast

# start snippet evaluate
def mean_absolute_error(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

y_test = test["level"].to_list()
naive_mae = mean_absolute_error(y_test, naive_pred)
trend_mae = mean_absolute_error(y_test, trend_pred)
print(f"naive MAE:          {naive_mae:.3f} m")
print(f"trend+seasonal MAE: {trend_mae:.3f} m")
# end snippet evaluate

# start snippet plot
plot_df = pl.DataFrame({
    "t": test["t"].to_list() * 3,
    "level": y_test + naive_pred + trend_pred,
    "series": ["actual"] * HOLDOUT + ["naive"] * HOLDOUT + ["trend+seasonal"] * HOLDOUT,
})

chart = alt.Chart(plot_df).mark_line().encode(
    x=alt.X("t:Q", title="month"),
    y=alt.Y("level:Q", title="river level (m)"),
    color=alt.Color("series:N", title=None),
)
chart.save("forecast.json")
# end snippet plot

# start snippet uncertainty
intercept, slope, seasonal, sigma = fit_trend_seasonal(t_train, y_train, PERIOD)
print(f"residual sigma: {sigma:.3f} m")
print(f"first forecast, +/- 2 sigma: {trend_pred[0]:.3f} m +/- {2 * sigma:.3f} m")
# end snippet uncertainty
