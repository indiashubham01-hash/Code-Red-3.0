import requests
try:
    r = requests.get("http://127.0.0.1:6969/health", timeout=2)
    print(r.status_code)
    print(r.json())
except Exception as e:
    print(e)
