from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import time
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# --- 1. APP INITIALIZATION ---
app = FastAPI(
    title="PULSE ERA | API Monitoring Tool",
    description="Backend for monitoring website health and latency"
)

# ... (Baaki code waisa hi rahega)

# --- 5. API ENDPOINTS ---

@app.get("/")
async def root():
    """Health check endpoint for Vercel"""
    return {
        "Project": "Pulse Era Backend",
        "Status": "Online",
        "System_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/status")
async def get_grid_status():
    """Saari monitored sites ka status ek saath check karta hai."""
    # asyncio.gather parallel processing ke liye best hai
    tasks = [probe_node(url) for url in monitored_nodes]
    results = await asyncio.gather(*tasks)
    return results

@app.post("/add-website")
async def add_node(node: Website):
    """Nayi website list mein add karta hai."""
    clean_url = node.url.strip()
    if not clean_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    if clean_url not in monitored_nodes:
        monitored_nodes.append(clean_url)
        return {"status": "SYNCED", "added": clean_url}
    
    return {"status": "ALREADY_EXISTS"}

@app.get("/list")
async def list_nodes():
    """Monitored URLs ki list dikhata hai."""
    return {"monitored_sites": monitored_nodes}

# --- 6. LAUNCH ---
if __name__ == "__main__":
    import uvicorn
    # Vercel mein ye part execute nahi hota, ye sirf local testing ke liye hai
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)    
    
    
@app.get("/")
def home():
    return {"status": "Pulse Era API is Running", "version": "1.0"}

# --- 2. CORS MIDDLEWARE (Zaroori for Deployment) ---
# Iske baghair aapka frontend API ko call nahi kar sakega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein yahan specific domains allow karein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. DATA MODELS ---
class Website(BaseModel):
    url: str

# Default monitoring list (Memory-based)
monitored_nodes = ["https://www.google.com", "https://www.github.com", "https://www.python.org"]

# --- 4. CORE LOGIC: PROBE FUNCTION ---
async def probe_node(url: str):
    """Website ko hit karta hai aur response time calculate karta hai."""
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    start_point = time.time()
    try:
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
            response = await client.get(url)
            latency = (time.time() - start_point) * 1000
            
            return {
                "URL": url, 
                "Status": "HEALTHY" if response.status_code == 200 else "UNSTABLE", 
                "HTTP_Code": response.status_code,
                "Latency_ms": round(latency, 2), 
                "Last_Check": datetime.now().strftime("%H:%M:%S")
            }
    except Exception as e:
        return {
            "URL": url, 
            "Status": "OFFLINE", 
            "HTTP_Code": "ERR", 
            "Latency_ms": 0.0, 
            "Last_Check": datetime.now().strftime("%H:%M:%S")
        }

# --- 5. API ENDPOINTS ---

@app.get("/")
async def root():
    """Health check endpoint for Vercel"""
    return {
        "Project": "Pulse Era Backend",
        "Status": "Online",
        "System_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/status")
async def get_grid_status():
    """Saari monitored sites ka status ek saath check karta hai."""
    # asyncio.gather parallel processing ke liye best hai
    tasks = [probe_node(url) for url in monitored_nodes]
    results = await asyncio.gather(*tasks)
    return results

@app.post("/add-website")
async def add_node(node: Website):
    """Nayi website list mein add karta hai."""
    clean_url = node.url.strip()
    if not clean_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    if clean_url not in monitored_nodes:
        monitored_nodes.append(clean_url)
        return {"status": "SYNCED", "added": clean_url}
    
    return {"status": "ALREADY_EXISTS"}

@app.get("/list")
async def list_nodes():
    """Monitored URLs ki list dikhata hai."""
    return {"monitored_sites": monitored_nodes}