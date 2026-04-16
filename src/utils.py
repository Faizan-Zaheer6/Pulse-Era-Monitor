import json
import os

# Data folder ka rasta
DB_PATH = "data/urls.json"

def load_urls():
    """JSON file se URLs ki list load karta hai."""
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_url(url):
    """Naya URL JSON file mein save karta hai."""
    urls = load_urls()
    if url not in urls:
        urls.append(url)
        # Agar data folder nahi bana to bana lo
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w") as f:
            json.dump(urls, f, indent=4)
        return True
    return False

def remove_url(url):
    """URL ko JSON file se delete karta hai."""
    urls = load_urls()
    if url in urls:
        urls.remove(url)
        with open(DB_PATH, "w") as f:
            json.dump(urls, f, indent=4)
        return True
    return False