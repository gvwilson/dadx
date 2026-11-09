# start snippet mock_server_imports
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
# end snippet mock_server_imports

# start snippet mock_data
REPORTS = [
    {"id": 1, "event": "cyclone", "severity": 4, "latitude": -32.5, "longitude": 141.2, "reported": "2024-06-01T08:12:00"},
    {"id": 2, "event": "flash-flood", "severity": 3, "latitude": -33.1, "longitude": 142.9, "reported": "2024-06-01T13:05:00"},
    {"id": 3, "event": "windstorm", "severity": 2, "latitude": -31.8, "longitude": 143.5, "reported": "2024-06-02T09:30:00"},
    {"id": 4, "event": "cyclone", "severity": 5, "latitude": -32.2, "longitude": 141.8, "reported": "2024-06-03T18:45:00"},
    {"id": 5, "event": "hail", "severity": 1, "latitude": -34.0, "longitude": 140.6, "reported": "2024-06-04T11:20:00"},
    {"id": 6, "event": "flash-flood", "severity": 2, "latitude": -32.9, "longitude": 142.1, "reported": "2024-06-05T07:55:00"},
]
PAGE_SIZE = 3
# end snippet mock_data

# start snippet storm_handler
class StormHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        page = int(query.get("page", ["1"])[0])
        start = (page - 1) * PAGE_SIZE
        items = REPORTS[start : start + PAGE_SIZE]
        next_page = page + 1 if start + PAGE_SIZE < len(REPORTS) else None
        body = json.dumps({"page": page, "next": next_page, "items": items}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
# end snippet storm_handler

# start snippet start_server
server = ThreadingHTTPServer(("127.0.0.1", 0), StormHandler)
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE_URL = f"http://127.0.0.1:{port}"
# end snippet start_server

# start snippet fetch_with_cache
import httpx

cache = {}
fetch_count = 0

def fetch(url):
    global fetch_count
    if url in cache:
        return cache[url]
    fetch_count += 1
    response = httpx.get(url)
    response.raise_for_status()
    data = response.json()
    cache[url] = data
    return data
# end snippet fetch_with_cache

# start snippet paginate
import time

def fetch_all(base_url):
    rows = []
    page = 1
    while True:
        url = f"{base_url}/reports?page={page}"
        data = fetch(url)
        rows.extend(data["items"])
        if data["next"] is None:
            break
        page = data["next"]
        time.sleep(0.05)
    return rows

reports = fetch_all(BASE_URL)
print("reports:", len(reports))
print("HTTP requests so far:", fetch_count)
# end snippet paginate

# start snippet transform
def transform(item):
    return (
        item["id"],
        item["event"],
        item["severity"],
        item["latitude"],
        item["longitude"],
        item["reported"],
    )

rows = [transform(r) for r in reports]
print(rows[0])
# end snippet transform

# start snippet load
import duckdb

con = duckdb.connect(":memory:")
con.execute("""
CREATE TABLE storm_reports (
    id INTEGER,
    event VARCHAR,
    severity INTEGER,
    latitude DOUBLE,
    longitude DOUBLE,
    reported TIMESTAMP
)
""")
# end snippet load

# start snippet insert
con.executemany("INSERT INTO storm_reports VALUES (?, ?, ?, ?, ?, ?)", rows)
print(con.execute("SELECT COUNT(*) FROM storm_reports").fetchone())
# end snippet insert

# start snippet query
print(
    con.execute(
        """
        SELECT event, COUNT(*) AS n, AVG(severity) AS avg_severity
        FROM storm_reports
        GROUP BY event
        ORDER BY n DESC
        """
    ).fetchall()
)
# end snippet query

# start snippet rerun_from_cache
reports_again = fetch_all(BASE_URL)
print("reports:", len(reports_again))
print("HTTP requests so far:", fetch_count)
# end snippet rerun_from_cache
