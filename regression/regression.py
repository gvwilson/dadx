# start snippet generate
import math
import random

import polars as pl

random.seed(1234)

n = 200
intercept = 5.0
slope_severity = 3.0
slope_distance = 0.4

severities = []
distances = []
response_times = []
for _ in range(n):
    severity = random.randint(1, 5)
    distance = random.uniform(0.5, 20.0)
    noise = random.gauss(0.0, 4.0)
    severities.append(severity)
    distances.append(distance)
    response_times.append(intercept + slope_severity * severity + slope_distance * distance + noise)

data = pl.DataFrame({
    "severity": severities,
    "distance_km": distances,
    "response_min": response_times,
})
print(data.head())
# end snippet generate


# start snippet normal_equations
def solve_linear(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = col
        best = abs(m[col][col])
        for r in range(col + 1, n):
            if abs(m[r][col]) > best:
                best = abs(m[r][col])
                pivot = r
        if best < 1e-12:
            raise ValueError("singular matrix")
        m[col], m[pivot] = m[pivot], m[col]
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= factor * m[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        total = m[r][n]
        for c in range(r + 1, n):
            total -= m[r][c] * x[c]
        x[r] = total / m[r][r]
    return x


def fit_least_squares(X, y):
    """Return the coefficients w that minimize the squared residuals."""
    n = len(X)
    p = len(X[0])
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for i in range(n):
        row = X[i]
        for j in range(p):
            xty[j] += row[j] * y[i]
            for k in range(p):
                xtx[j][k] += row[j] * row[k]
    return solve_linear(xtx, xty)


def predict(X, w):
    """Return the fitted value for each row: its dot product with w."""
    return [sum(row[j] * w[j] for j in range(len(w))) for row in X]
# end snippet normal_equations


# start snippet fit
X = [[1.0, float(s), d] for s, d in zip(severities, distances)]
y = list(response_times)

w = fit_least_squares(X, y)
print("coefficients (intercept, severity, distance):")
print(w)
# end snippet fit


# start snippet residuals
y_pred = predict(X, w)
residuals = [y[i] - y_pred[i] for i in range(n)]

print("mean residual:", sum(residuals) / len(residuals))
print("residual range:", min(residuals), "to", max(residuals))
# end snippet residuals


# start snippet evaluate
def mean_absolute_error(y_true, y_pred):
    """Average absolute difference between true and predicted values."""
    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)


random.seed(99)
idx = list(range(n))
random.shuffle(idx)
split = int(0.8 * n)

X_train = [X[i] for i in idx[:split]]
y_train = [y[i] for i in idx[:split]]
X_test = [X[i] for i in idx[split:]]
y_test = [y[i] for i in idx[split:]]

w_train = fit_least_squares(X_train, y_train)
y_train_pred = predict(X_train, w_train)
y_test_pred = predict(X_test, w_train)

print("training MAE:", mean_absolute_error(y_train, y_train_pred))
print("test MAE:", mean_absolute_error(y_test, y_test_pred))
# end snippet evaluate


# start snippet plot
import altair as alt

results = pl.DataFrame({
    "actual": y_test,
    "predicted": y_test_pred,
})

lo = min(min(y_test), min(y_test_pred))
hi = max(max(y_test), max(y_test_pred))
diag = pl.DataFrame({"v": [lo, hi]})

reference = alt.Chart(diag).mark_line(color="grey", strokeDash=[4, 4]).encode(
    x="v",
    y="v",
)

points = alt.Chart(results).mark_circle().encode(
    x=alt.X("actual", title="Actual response time (minutes)"),
    y=alt.Y("predicted", title="Predicted response time (minutes)"),
    tooltip=["actual", "predicted"],
)

chart = (reference + points).properties(
    width=400,
    height=400,
    title="Actual vs predicted on held-out incidents",
)

chart.save("regression.json")
# end snippet plot
