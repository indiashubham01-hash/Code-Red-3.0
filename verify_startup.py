import requests
import time

url = "http://127.0.0.1:6969/health"
print("Waiting for server...")
for i in range(15):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print("Server is UP!")
            models = res.json().get('models', {})
            print(f"Models status: {models}")
            break
    except:
        pass
    time.sleep(2)
else:
    print("Server failed to allow connection.")
