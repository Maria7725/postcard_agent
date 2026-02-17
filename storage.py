import json
from pathlib import Path

DB_FILE = Path("seen_items.json")

def load_seen_ids():
    if DB_FILE.exists():
        data = json.loads(DB_FILE.read_text())
        return set(data)
    return set()

def save_seen_ids(seen_ids):
    DB_FILE.write_text(json.dumps(list(seen_ids)))
