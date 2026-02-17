import requests
from auth import get_access_token

SEARCH_URL = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"

token = get_access_token()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

params = {
    "q": "postcard",
    "limit": 5,
}

response = requests.get(SEARCH_URL, headers=headers, params=params)
print("Status:", response.status_code)
# print(response.text[:500])  # print first 500 chars to avoid huge output

data = response.json()

total = data.get("total", 0)
print("Total results", total)

items = data.get("itemSummaries", [])

if not items:
    print("No items found in Sandbox (this is normal).")
else:
      for item in items:
        title = item.get("title")
        price = item.get("price", {}).get("value")
        url = item.get("itemWebUrl")
        print("-", title, "|", price, "|", url)  