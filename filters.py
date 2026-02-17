def is_interesting(item, keywords, min_price, max_price):
    """
    Returns True if the item matches keywords and price range.
    """
    title_lower = item["title"].lower()

    # Price filter
    if not (min_price <= item["price"] <= max_price):
        return False

    # Keyword filter
    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True

    return False
