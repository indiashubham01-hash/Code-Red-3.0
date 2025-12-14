import requests
import sys

BASE_URL = "http://127.0.0.1:6969"

def check_frontend():
    print(f"Checking Frontend at {BASE_URL}...")
    try:
        res = requests.get(BASE_URL)
        if res.status_code == 200 and "<!doctype html>" in res.text.lower():
            print("[SUCCESS] Frontend loaded (HTML found).")
        else:
            print(f"[FAIL] Frontend check failed. Status: {res.status_code}")
            # print(res.text[:200])
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

def check_model_api():
    print(f"\nChecking API at {BASE_URL}/health...")
    try:
        res = requests.get(f"{BASE_URL}/health")
        if res.status_code == 200:
            print("[SUCCESS] API is healthy.")
            print(res.json())
        else:
            print(f"[FAIL] API health check failed. Status: {res.status_code}")
    except Exception as e:
        print(f"[ERROR] API Connection failed: {e}")

if __name__ == "__main__":
    check_frontend()
    check_model_api()
