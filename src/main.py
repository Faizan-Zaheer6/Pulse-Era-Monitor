from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import asyncio
import time
from datetime import datetime

app = FastAPI(title="PULSE ERA | Backend")

class Website(BaseModel):
    url: str

# Default data taake stats gaib na hon
monitored_nodes = ["https://www.google.com", "https://www.github.com", "https://www.python.org"]

async def probe_node(url: str):
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    start_point = time.time()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            latency = (time.time() - start_point) * 1000
            return {
                "URL": url, 
                "Status": "HEALTHY" if response.status_code == 200 else "UNSTABLE", 
                "HTTP Code": str(response.status_code),
                "Latency (ms)": round(latency, 2), 
                "Time": datetime.now().strftime("%H:%M:%S")
            }
    except:
        return {
            "URL": url, "Status": "OFFLINE", "HTTP Code": "ERR", 
            "Latency (ms)": 0.0, "Time": datetime.now().strftime("%H:%M:%S")
        }

@app.get("/status")
async def get_grid_status():
    tasks = [probe_node(url) for url in monitored_nodes]
    return await asyncio.gather(*tasks)

@app.post("/add-website")
async def add_node(node: Website):
    clean_url = node.url.strip()
    if clean_url and clean_url not in monitored_nodes:
        monitored_nodes.append(clean_url)
    return {"status": "SYNCED"}