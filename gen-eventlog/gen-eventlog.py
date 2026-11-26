# mccole:imports
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 20261108
random.seed(SEED)
# mccole:/imports

# mccole:write_csv
def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
# mccole:/write_csv

# mccole:make_responders
FIRST = ["Ada", "Grace", "Alan", "Edsger", "Barbara", "Donald", "Kathleen", "John"]
LAST = ["Lovelace", "Hopper", "Turing", "Dijkstra", "Liskov", "Knuth", "Booth", "Backus"]
ROLES = ["dispatcher", "field-officer", "medic", "coordinator"]

def make_responders(n):
    start = date(2024, 1, 1)
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "id": i,
            "name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "joined": (start + timedelta(days=random.randint(0, 365))).isoformat(),
            "role": random.choice(ROLES),
        })
    return rows
# mccole:/make_responders

# mccole:make_sites
HABITATS = ["forest", "wetland", "grassland", "riparian"]

def make_sites(n):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "id": i,
            "latitude": round(random.uniform(-40.0, -30.0), 4),
            "longitude": round(random.uniform(140.0, 150.0), 4),
            "habitat": random.choice(HABITATS),
        })
    return rows
# mccole:/make_sites

# mccole:make_incidents
KINDS = ["storm", "flood", "power-outage", "fire"]
STATUSES = ["reported", "triaged", "dispatched", "resolved"]

def make_incidents(n, n_responders):
    base = datetime(2024, 6, 1, 0, 0, 0)
    rows = []
    for i in range(1, n + 1):
        when = base + timedelta(
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
# mccole:/make_incidents

# mccole:make_observations
SPECIES = {
    "forest": ["koala", "lyrebird", "wombat"],
    "wetland": ["frog", "ibis", "platypus"],
    "grassland": ["kangaroo", "eagle", "skink"],
    "riparian": ["crayfish", "kingfisher", "water-rat"],
}

def make_observations(n, sites):
    rows = []
    for i in range(1, n + 1):
        site = random.choice(sites)
        rows.append({
            "id": i,
            "site_id": site["id"],
            "species": random.choice(SPECIES[site["habitat"]]),
            "count": random.randint(1, 12),
            "mass_g": round(random.uniform(1.0, 5000.0), 1),
            "length_mm": round(random.uniform(10.0, 800.0), 1),
            "date": (date(2024, 3, 1) + timedelta(days=random.randint(0, 90))).isoformat(),
        })
    return rows
# mccole:/make_observations

# mccole:write_files
responders = make_responders(20)
write_csv(Path("responders.csv"), ["id", "name", "joined", "role"], responders)

incidents = make_incidents(120, len(responders))
write_csv(
    Path("incidents.csv"),
    ["id", "timestamp", "latitude", "longitude", "kind", "severity", "status", "responder_id"],
    incidents,
)

sites = make_sites(8)
write_csv(Path("sites.csv"), ["id", "latitude", "longitude", "habitat"], sites)

observations = make_observations(90, sites)
write_csv(
    Path("observations.csv"),
    ["id", "site_id", "species", "count", "mass_g", "length_mm", "date"],
    observations,
)
# mccole:/write_files

# mccole:verify_join
import polars as pl

responders = pl.read_csv("responders.csv")
incidents = pl.read_csv("incidents.csv")
disaster = incidents.join(
    responders.rename({"id": "responder_id"}), on="responder_id", how="left"
)
print("disaster rows:", disaster.shape)
print(disaster.select(["id", "kind", "name", "role"]).head(3))

sites = pl.read_csv("sites.csv")
observations = pl.read_csv("observations.csv")
ecology = observations.join(sites, left_on="site_id", right_on="id", how="left")
print("ecology rows:", ecology.shape)
print(ecology.select(["id", "species", "habitat"]).head(3))
# mccole:/verify_join
