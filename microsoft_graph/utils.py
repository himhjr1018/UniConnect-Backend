import requests
from . import config
from datetime import datetime, timedelta


OUTLOOK_CONTACTS_API = "https://graph.microsoft.com/v1.0/me/contacts"


def graph_call(api, access_token, data={}, method="GET"):
    headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
    }
    # make graph call
    if method == "GET":
        resp = requests.get(api, headers=headers)
    elif method == "POST":
        resp =requests.post(api, json=data, headers=headers)
    return resp


def refresh_access_token(profile):
    graph_token_api = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    post_data = {
            "client_id": config.clientId,
            "scope": config.graphUserScopes,
            "grant_type": "refresh_token",
            "client_secret": config.clientSecret,
            "redirect_uri": config.accessRedirectUri,
            "refresh_token": profile.con_refresh_token,
        }
    # refresh_access_token
    resp = requests.post(graph_token_api, data=post_data).json()
    profile.con_access_token = resp["access_token"]
    profile.con_connected = True
    profile.con_access_expiry = datetime.now() + timedelta(minutes=50)
    profile.save()

