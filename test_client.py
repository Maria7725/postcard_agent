from config import KEYWORDS
from ebay_client import search_postcards

query = " OR ".join(KEYWORDS)   # eBay treats this as a broader query
items = search_postcards(query, limit=20)

print(f"Query used: {query}")
print(f"Found {len(items)} items:\n")

for i, item in enumerate(items, start=1):
    print(f"{i}. {item['title']}")
    print(f"   Price: ${item['price']}")
    ship = item.get("shipping")
    ship_str = f"${ship:.2f}" if ship is not None else "N/A"
    print(f"   Shipping to Palmer: {ship_str}")
    print(f"   URL:   {item['url']}")
    print("-" * 60)
