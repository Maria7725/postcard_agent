import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from auth import get_access_token

load_dotenv()

ENV = os.getenv("EBAY_ENV", "production")

if ENV == "sandbox":
    SEARCH_URL = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"
else:
    SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

SHIP_TO_ZIP = os.getenv("EBAY_SHIP_TO_ZIP") 
SHIP_TO_COUNTRY = os.getenv("EBAY_SHIP_TO_COUNTRY")

def _extract_shipping_cost(item: dict):
    shipping_options = item.get("shippingOptions") or []
    if not shipping_options:
        return None

    shipping_cost = shipping_options[0].get("shippingCost") or {}
    value = shipping_cost.get("value")
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def search_postcards(query, limit=10):
    token = get_access_token()

    # Important: ship-to context so eBay calculates shipping for Palmer
    enduserctx_raw = f"contextualLocation=country={SHIP_TO_COUNTRY},zip={SHIP_TO_ZIP}"
    enduserctx_encoded = quote(enduserctx_raw, safe="=,")  # keep '=' and ',' unescaped

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "X-EBAY-C-ENDUSERCTX": enduserctx_encoded,
    }

    params = {
        "q": query,
        "limit": limit,
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    items = data.get("itemSummaries", [])

    results = []
    for item in items:
        results.append({
            "id": item.get("itemId"),
            "title": item.get("title"),
            "price": float(item.get("price", {}).get("value", 0) or 0),
            "shipping": _extract_shipping_cost(item),
            "url": item.get("itemWebUrl"),
        })

    return results
