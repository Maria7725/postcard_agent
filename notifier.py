def _print_items(title, items):
    print("\n" + title)
    print("=" * len(title))

    if not items:
        print("(none)")
        return

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item.get('title')}")
        print(f"   Price: ${item.get('price')}")
        ship = item.get("shipping")
        ship_str = f"${ship:.2f}" if ship is not None else "N/A"
        print(f"   Shipping to Palmer: {ship_str}")
        print(f"   URL:   {item.get('url')}")
        print("-" * 60)


def notify(new_items, seen_items):
    _print_items("New listings", new_items)
    _print_items("Already seen", seen_items)
