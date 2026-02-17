import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("EBAY_ENV", "production")

if ENV == "sandbox":
    CLIENT_ID = os.getenv("EBAY_SANDBOX_CLIENT_ID")
    CLIENT_SECRET = os.getenv("EBAY_SANDBOX_CLIENT_SECRET")
    TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
else:
    CLIENT_ID = os.getenv("EBAY_PROD_CLIENT_ID")
    CLIENT_SECRET = os.getenv("EBAY_PROD_CLIENT_SECRET")
    TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

SCOPE = "https://api.ebay.com/oauth/api_scope"

def get_access_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError(f"Missing credentials for ENV={ENV}")

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    basic_auth = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth}",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": SCOPE,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
