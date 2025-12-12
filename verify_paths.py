import requests
import json

url = "http://127.0.0.1:8004/openapi.json"

try:
    print(f"Fetching {url}...")
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        paths = list(data.get("paths", {}).keys())
        print("Registered Paths:")
        for p in paths:
            print(p)
    else:
        print(f"Failed to get openapi.json: {res.status_code}")
except Exception as e:
    print(f"Error: {e}")
