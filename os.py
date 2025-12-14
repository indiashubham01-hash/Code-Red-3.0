import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found.")
else:
    try:
        client = genai.Client(api_key=api_key)
        # Try to list models if possible, or just try a simple generation with a known working model
        # The SDK might not have a list_models method easily accessible on the client directly in the same way as the old SDK.
        # Let's try to run a simple generation with gemini-1.5-flash
        print("Trying gemini-1.5-flash...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello",
        )
        print("Success with gemini-1.5-flash!")
        print(response.text)
    except Exception as e:
        print(f"Error with gemini-1.5-flash: {e}")

    try:
        print("\nTrying gemini-2.0-flash-exp...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Hello",
        )
        print("Success with gemini-2.0-flash-exp!")
        print(response.text)
    except Exception as e:
        print(f"Error with gemini-2.0-flash-exp: {e}")