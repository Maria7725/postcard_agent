from ebay_client import search_postcards
from filters import is_interesting
from storage import load_seen_ids, save_seen_ids
from notifier import notify  # we’ll update notifier next
from config import KEYWORDS, MIN_PRICE, MAX_PRICE
from email_notifier import send_email

TEST_EMAIL_ALREADY_SEEN = False   # change to true if want to get email with already seen results

def main():
    print("Postcard agent starting...")

    seen_ids = load_seen_ids()

    # broad search; filter locally
    # query = "postcard (" + "OR ".join(KEYWORDS) +")"  # eBay treats this as a broader query
    query = "OR".join(KEYWORDS)
    items = search_postcards(query, limit=50)

    print("Fetched from eBay:", len(items))
    if items:
        print("First title:", items[0]["title"])

    new_matches = []
    seen_matches = []

    print("KEYWORDS:", KEYWORDS)
    print("MIN/MAX:", MIN_PRICE, MAX_PRICE)

    for item in items:
        if not is_interesting(item, KEYWORDS, MIN_PRICE, MAX_PRICE):
            #debug: show a few rejected titles
            print("Rejected:", item["title"])
            continue

        if item["id"] in seen_ids:
            seen_matches.append(item)
        else:
            new_matches.append(item)
            seen_ids.add(item["id"])  # mark as seen after first time

    # show both categories
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
