from ebay_client import search_postcards
from filters import is_interesting
from storage import load_seen_ids, save_seen_ids
from notifier import notify
from config import KEYWORDS, MIN_PRICE, MAX_PRICE
from email_notifier import send_email

TEST_EMAIL_ALREADY_SEEN = False


def main():
    print("Postcard agent starting...")

    seen_ids = load_seen_ids()

    # 1) Run one search per keyword exactly as written in config.py
    queries = [kw.strip() for kw in KEYWORDS if kw.strip()]
    print("Queries to run:")
    for q in queries:
        print(" -", q)

    # 2) Aggregate and deduplicate results by item id
    aggregated_by_id = {}
    for q in queries:
        items = search_postcards(q, limit=50)
        print(f"Fetched from eBay for '{q}': {len(items)}")
        for item in items:
            aggregated_by_id[item["id"]] = item

    items = list(aggregated_by_id.values())
    print("Total unique fetched items:", len(items))

    new_matches = []
    seen_matches = []

    print("KEYWORDS:", KEYWORDS)
    print("MIN/MAX:", MIN_PRICE, MAX_PRICE)

    for item in items:
        if not is_interesting(item, KEYWORDS, MIN_PRICE, MAX_PRICE):
            print("Rejected:", item["title"])
            continue

        if item["id"] in seen_ids:
            seen_matches.append(item)
        else:
            new_matches.append(item)
            seen_ids.add(item["id"])

    new_matches.sort(key=lambda x: x.get("price", 0))
    seen_matches.sort(key=lambda x: x.get("price", 0))

    notify(new_matches, seen_matches)

    if TEST_EMAIL_ALREADY_SEEN:
        print("TEST MODE: emailing already seen results")
        send_email(seen_matches)
    else:
        if new_matches:
            send_email(new_matches)

    save_seen_ids(seen_ids)


if __name__ == "__main__":
    main()
