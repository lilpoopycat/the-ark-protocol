# ark_core/comm.py
"""Communication (REST API) for Ark Protocol distributed agents."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import uvicorn
import threading

app = FastAPI()

# In-memory store for demonstration (replace with persistent store as needed)
shard_store = []
fitness_reports = []

@app.post("/shard/submit")
async def submit_shard(request: Request):
    shard = await request.json()
    shard_store.append(shard)
    return {"status": "received", "shard_id": shard.get("shard_id")}

@app.get("/shard/request")
def request_shard():
    # Return all shards for now (could filter by query params)
    return {"shards": shard_store}

@app.post("/fitness/report")
async def report_fitness(request: Request):
    report = await request.json()
    fitness_reports.append(report)
    return {"status": "fitness report received", "shard_id": report.get("shard_id")}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Client functions ---
def send_shard(shard, target_url):
    resp = requests.post(f"{target_url}/shard/submit", json=shard)
    return resp.json()

def request_shards(target_url):
    resp = requests.get(f"{target_url}/shard/request")
    return resp.json()

def send_fitness_report(report, target_url):
    resp = requests.post(f"{target_url}/fitness/report", json=report)
    return resp.json()

# --- Server runner ---
def run_server(host="0.0.0.0", port=8000, background=True):
    if background:
        thread = threading.Thread(target=uvicorn.run, args=("ark_core.comm:app",), kwargs={"host": host, "port": port, "log_level": "info"}, daemon=True)
        thread.start()
    else:
        uvicorn.run("ark_core.comm:app", host=host, port=port, log_level="info") 