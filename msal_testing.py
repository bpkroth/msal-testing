#!/usr/bin/env python3
import base64
from datetime import datetime, timedelta
import json
import time
import secretstorage
from msal import PublicClientApplication

# ---- CONFIG ----
CLIENT_ID = "872cd9fa-d31f-45e0-9eab-6e460a02d1f1"  # usually GCM has a known client id
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPE = ["499b84ac-1321-427f-aa17-267ca6975798/.default"]  # ADO default scope

def get_secret_collection():
    bus = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(bus)
    for item in collection.get_all_items():
        print(f"Item: {item.get_label()}, Attributes: {item.get_attributes()}")
    return collection

def get_item(k, v, account=None):
    collection = get_secret_collection()
    items = collection.search_items({k: v})
    for item in items:
        if account is None or item.get_attributes().get("account") == account:
            return item.get_secret().decode()
    return None

def get_secret(service, account=None):
    items = get_item("service", service, account)
    for item in items:
        if account is None or item.get_attributes().get("account") == account:
            return item.get_secret().decode()
    return None

def main():
    # 1. Try to get RefreshToken from SecretService
    #secret = get_secret("git:https://dev.azure.com/", None)
    secret_b64 = get_item("MsalClientID", "Microsoft.Developer.IdentityService")
    if secret_b64 is None:
        print("No matching Secret found in SecretService.")
        return
    secret_json = base64.b64decode(secret_b64).decode('utf-8')
    secret = json.loads(secret_json)
    print(f"Found secret in SecretService: {json.dumps(secret, indent=2)}\n")
    refresh_token = secret.get("RefreshToken")
    if refresh_token is None:
        print("No RefreshToken found in the secret.")
        return

    # Pick the first instance that has a secret
    refresh_token_secret = None
    for k,v in refresh_token.items():
        if v.get("secret") is not None:
            refresh_token = v
            refresh_token_secret = v["secret"]
            break
    print(f"Found RefreshToken in SecretService: {json.dumps(refresh_token, indent=2)}\n")

    # 2. Initialize MSAL PublicClientApplication
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)

    # 3. Try to acquire token silently using the refresh token
    token_response = app.acquire_token_by_refresh_token(
        refresh_token_secret, scopes=SCOPE,
    )

    print()

    if "access_token" in token_response:
        print(f"Successfully acquired new AccessToken! {json.dumps(token_response, indent=2)}\n")
        print("Expires at:", datetime.now() + timedelta(seconds=token_response["expires_in"]))
    else:
        print("Failed to acquire AccessToken via RefreshToken.")
        print(json.dumps(token_response, indent=2))

if __name__ == "__main__":
    main()
