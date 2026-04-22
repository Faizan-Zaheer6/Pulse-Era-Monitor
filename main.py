from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
from datetime import datetime
from typing import List

app = FastAPI()

# --- 1. MODEL DEFINITION (Missing in your previous logs) ---
class Website(BaseModel):
    url: str

# Monitoring list
db_websites = ["https://www.google.com", "https://www.github.com", "https://www.python.org"]

# --- 2. ROOT ROUTE ---
@app.get("/")
def home():
    return {"status": "Pulse Era API is Running"}

# --- 3. STATUS ROUTE ---
@app.get("/status")
async def get_status():
    results = []
    async with httpx.AsyncClient() as client:
        for url in db_websites:
            try:
                start_time = datetime.now()
                response = await client.get(url, timeout=5.0)
                latency = (datetime.now() - start_time).total_seconds() * 1000
                results.append({
                    "URL": url,
                    "Status": "HEALTHY" if response.status_code == 200 else "UNHEALTHY",
                    "HTTP_Code": response.status_code,
                    "Latency_ms": round(latency, 2),
                    "Last_Check": datetime.now().strftime("%H:%M:%S")
                })
            except Exception:
                results.append({"URL": url, "Status": "DOWN", "HTTP_Code": 0, "Latency_ms": 0, "Last_Check": datetime.now().strftime("%H:%M:%S")})
    return results

# --- 4. ADD WEBSITE ROUTE ---
@app.post("/add-website")
async def add_node(node: Website):
    clean_url = node.url.strip()
    if not clean_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    if clean_url not in db_websites:
        db_websites.append(clean_url)
        return {"status": "SYNCED", "added": clean_url}
    
    return {"status": "ALREADY_EXISTS"}