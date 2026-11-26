# mccole:setup
import random
from datetime import date, datetime, timedelta

import duckdb
import polars as pl

SEED = 20261108
random.seed(SEED)
# mccole:/setup

# mccole:responders
FIRST = ["Ada", "Grace", "Alan", "Edsger", "Barbara", "Donald", "Kathleen", "John"]
LAST = ["Lovelace", "Hopper", "Turing", "Dijkstra", "Liskov", "Knuth", "Booth", "Backus"]
ROLES = ["dispatcher", "field-officer", "medic", "coordinator"]

start = date(2024, 1, 1)
responders = pl.DataFrame({
    "id": range(1, 9),
    "name": [f"{random.choice(FIRST)} {random.choice(LAST)}" for _ in range(8)],
    "joined": [(start + timedelta(days=random.randint(0, 365))).isoformat() for _ in range(8)],
    "role": [random.choice(ROLES) for _ in range(8)],
})
print(responders)
# mccole:/responders

# mccole:incidents
KINDS = ["storm", "flood", "power-outage", "fire"]
STATUSES = ["reported", "triaged", "dispatched", "resolved"]

n = 24
base = datetime(2024, 6, 1)
incidents = pl.DataFrame({
    "id": range(1, n + 1),
    "timestamp": [
        (base + timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))).isoformat()
        for _ in range(n)
    ],
    "latitude": [round(random.uniform(-40.0, -30.0), 4) for _ in range(n)],
    "longitude": [round(random.uniform(140.0, 150.0), 4) for _ in range(n)],
    "kind": [random.choice(KINDS) for _ in range(n)],
    "severity": [random.randint(1, 5) for _ in range(n)],
    "status": [random.choice(STATUSES) for _ in range(n)],
    "responder_id": [random.randint(1, 8) for _ in range(n)],
})
print(incidents)
# mccole:/incidents

# mccole:load
con = duckdb.connect()

con.execute("""
CREATE TABLE responders (
    id INTEGER,
    name VARCHAR,
    joined DATE,
    role VARCHAR
)
""")
con.executemany(
    "INSERT INTO responders VALUES (?, ?, ?, ?)",
    responders.rows(),
)

con.execute("""
CREATE TABLE incidents (
    id INTEGER,
    timestamp TIMESTAMP,
    latitude DOUBLE,
    longitude DOUBLE,
    kind VARCHAR,
    severity INTEGER,
    status VARCHAR,
    responder_id INTEGER
)
""")
con.executemany(
    "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    incidents.rows(),
)
# mccole:/load

# mccole:select_sql
print(con.execute("SELECT id, kind, severity FROM incidents LIMIT 3").fetchall())
# mccole:/select_sql

# mccole:select_polars
print(incidents.select(["id", "kind", "severity"]).head(3))
# mccole:/select_polars

# mccole:where_sql
print(con.execute("""
SELECT id, kind, severity
FROM incidents
WHERE severity >= 4
ORDER BY severity DESC
""").fetchall())
# mccole:/where_sql

# mccole:where_polars
print(
    incidents
    .filter(pl.col("severity") >= 4)
    .select(["id", "kind", "severity"])
    .sort("severity", descending=True)
)
# mccole:/where_polars

# mccole:group_by_sql
print(con.execute("""
SELECT kind, COUNT(*) AS n
FROM incidents
GROUP BY kind
ORDER BY n DESC
""").fetchall())
# mccole:/group_by_sql

# mccole:group_by_polars
print(incidents.group_by("kind").agg(pl.len().alias("n")).sort("n", descending=True))
# mccole:/group_by_polars

# mccole:join_sql
print(con.execute("""
SELECT i.id, i.kind, r.name
FROM incidents AS i
JOIN responders AS r ON i.responder_id = r.id
ORDER BY i.id
LIMIT 5
""").fetchall())
# mccole:/join_sql

# mccole:join_polars
print(
    incidents
    .join(responders, left_on="responder_id", right_on="id", how="inner")
    .select(["id", "kind", "name"])
    .head(5)
)
# mccole:/join_polars

# mccole:aggregate_sql
print(con.execute("""
SELECT status, COUNT(*) AS n, ROUND(AVG(severity), 2) AS avg_severity
FROM incidents
GROUP BY status
ORDER BY n DESC
""").fetchall())
# mccole:/aggregate_sql

# mccole:aggregate_polars
print(
    incidents
    .group_by("status")
    .agg(
        pl.len().alias("n"),
        pl.col("severity").mean().round(2).alias("avg_severity"),
    )
    .sort("n", descending=True)
)
# mccole:/aggregate_polars
