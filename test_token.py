from auth import get_access_token

token = get_access_token()
print("Token received (first 20 chars):", token[:20])
