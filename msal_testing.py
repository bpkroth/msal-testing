#!/usr/bin/env python3
import json
import time
import secretstorage
from msal import PublicClientApplication

# ---- CONFIG ----
CLIENT_ID = "872cd9fa-d31f-45e0-9eab-6e460a02d1f1"  # usually GCM has a known client id
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPE = ["499b84ac-1321-427f-aa17-267ca6975798/.default"]  # ADO default scope

def get_secret(service, account=None):
    bus = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(bus)
    items = collection.search_items({"service": service})
    for item in items:
        if account is None or item.get_attributes().get("account") == account:
            return item.get_secret().decode()
    return None

def main():
    # 1. Try to get RefreshToken from SecretService
    refresh_token = get_secret("git:https://dev.azure.com/", None)
    if refresh_token is None:
        print("No RefreshToken found in SecretService.")
        return

    print("Found RefreshToken in SecretService.")

    # 2. Initialize MSAL PublicClientApplication
    app = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)

    # 3. Try to acquire token silently using the refresh token
    token_response = app.acquire_token_by_refresh_token(
        refresh_token, scopes=SCOPE
    )

    if "access_token" in token_response:
        print("Successfully acquired new AccessToken!")
        print("Expires at:", time.ctime(token_response["expires_on"]))
    else:
        print("Failed to acquire AccessToken via RefreshToken.")
        print(json.dumps(token_response, indent=2))

if __name__ == "__main__":
    main()
