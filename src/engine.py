import httpx
import time
import asyncio

async def get_site_health(url: str):
    """
    Kisi bhi URL ki health aur performance details nikaalne ka function.
    """
    if not url.startswith("http"):
        url = "https://" + url
        
    start_time = time.time()
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Request bhej rahe hain
            response = await client.get(url, timeout=10.0)
            end_time = time.time()
            
            latency = round((end_time - start_time) * 1000, 2) # Milliseconds mein
            
            return {
                "URL": url,
                "Status": "Healthy" if response.status_code == 200 else "Issues",
                "HTTP Code": response.status_code,
                "Latency (ms)": latency,
                "Server": response.headers.get("server", "N/A"),
                "Size (KB)": round(len(response.content) / 1024, 2)
            }
    except Exception as e:
        return {
            "URL": url,
            "Status": "Down",
            "HTTP Code": "Error",
            "Latency (ms)": 0,
            "Server": "N/A",
            "Size (KB)": 0
        }