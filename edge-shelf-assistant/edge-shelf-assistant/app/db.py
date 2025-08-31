import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "products.json"

def load_products():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def query_by_keyword(keyword: str):
    keyword = keyword.lower()
    results = {}
    for name, meta in load_products().items():
        if keyword in name.lower():
            results[name] = meta
    return results

def get_all():
    return load_products()
