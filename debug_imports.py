print("1. Start")
try:
    import fastapi
    print("2. fastapi imported")
except ImportError as e: print(f"Error: {e}")

try:
    import torch
    print("3. torch imported")
except ImportError as e: print(f"Error: {e}")

try:
    from google import genai
    print("4. google.genai imported")
except ImportError as e: print(f"Error: {e}")

print("5. Done")
