# mccole:imports
import json
from datetime import datetime, timezone

import polars as pl

KINDS = ["storm", "flood", "power-outage", "fire"]
STATUSES = ["reported", "triaged", "dispatched", "resolved"]
SEVERITIES = ["low", "medium", "high"]
# mccole:/imports

# mccole:dictionary
dictionary = [
    {"name": "id", "type": "integer", "units": None,
     "meaning": "unique identifier for an incident", "allowed": None},
    {"name": "timestamp", "type": "datetime", "units": None,
     "meaning": "when the incident was reported", "allowed": None},
    {"name": "latitude", "type": "float", "units": "decimal degrees",
     "meaning": "north-south position", "allowed": "between -40.0 and -30.0"},
    {"name": "longitude", "type": "float", "units": "decimal degrees",
     "meaning": "east-west position", "allowed": "between 140.0 and 150.0"},
    {"name": "kind", "type": "string", "units": None,
     "meaning": "the type of incident", "allowed": KINDS},
    {"name": "severity", "type": "string", "units": None,
     "meaning": "how serious the incident is", "allowed": SEVERITIES},
    {"name": "status", "type": "string", "units": None,
     "meaning": "where the incident sits in the response workflow", "allowed": STATUSES},
    {"name": "responder_id", "type": "integer", "units": None,
     "meaning": "id of the responder assigned", "allowed": "id present in responders"},
]
# mccole:/dictionary

# mccole:describe
def describe(allowed):
    return ", ".join(allowed) if isinstance(allowed, list) else allowed

dd = pl.DataFrame([{**row, "allowed": describe(row["allowed"])} for row in dictionary])
print(dd)
# mccole:/describe

# mccole:query_dictionary
print(dd.filter(pl.col("units").is_not_null()).select("name", "units"))
# mccole:/query_dictionary

# mccole:categorical_fields
print([row["name"] for row in dictionary if isinstance(row["allowed"], list)])
# mccole:/categorical_fields

# mccole:validate
def check_allowed(frame, dictionary):
    problems = []
    for row in dictionary:
        if not isinstance(row["allowed"], list):
            continue
        name = row["name"]
        for value in frame[name].to_list():
            if value not in row["allowed"]:
                problems.append((name, value))
    return problems
# mccole:/validate

# mccole:incidents
incidents = pl.DataFrame([
    {"id": 1, "timestamp": "2024-06-01T08:12:00", "latitude": -33.86,
     "longitude": 151.21, "kind": "storm", "severity": "high",
     "status": "reported", "responder_id": 3},
    {"id": 2, "timestamp": "2024-06-01T08:30:00", "latitude": -33.87,
     "longitude": 151.20, "kind": "Flood", "severity": "medium",
     "status": "triaged", "responder_id": 3},
    {"id": 3, "timestamp": "2024-06-01T09:05:00", "latitude": -34.00,
     "longitude": 150.90, "kind": "fire", "severity": "critical",
     "status": "dispatched", "responder_id": 7},
])
# mccole:/incidents

# mccole:check_contract
print(check_allowed(incidents, dictionary))
# mccole:/check_contract

# mccole:provenance_log
provenance = []

def log_step(name, inputs, outputs):
    entry = {
        "step": name,
        "inputs": inputs,
        "outputs": outputs,
        "time": datetime.now(timezone.utc).isoformat(),
    }
    provenance.append(entry)
    return entry
# mccole:/provenance_log

# mccole:run_pipeline
log_step("load", [], ["incidents"])

cleaned = incidents.with_columns(pl.col("kind").str.to_lowercase())
log_step("normalize", ["incidents"], ["cleaned"])

counts = cleaned.group_by("kind").len()
log_step("summarize", ["cleaned"], ["counts_by_kind"])
# mccole:/run_pipeline

# mccole:write_log
with open("provenance.jsonl", "w") as f:
    for entry in provenance:
        f.write(json.dumps(entry) + "\n")
# mccole:/write_log

# mccole:read_back
log = pl.read_ndjson("provenance.jsonl")
print(log)
# mccole:/read_back

# mccole:query_log
print(log.filter(pl.col("step") == "summarize").select("inputs", "outputs"))
# mccole:/query_log

# mccole:ecology_twin
observations_dict = [
    {"name": "species", "type": "string", "units": None,
     "meaning": "species identifier", "allowed": "controlled taxonomy"},
    {"name": "count", "type": "integer", "units": "individuals",
     "meaning": "number observed at the site", "allowed": "non-negative"},
    {"name": "mass_g", "type": "float", "units": "grams",
     "meaning": "mass of the sample", "allowed": "positive"},
    {"name": "length_mm", "type": "float", "units": "millimeters",
     "meaning": "length of the sample", "allowed": "positive"},
]
print(pl.DataFrame([{**row, "allowed": describe(row["allowed"])} for row in observations_dict]))
# mccole:/ecology_twin
