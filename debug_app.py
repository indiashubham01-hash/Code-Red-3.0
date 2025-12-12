import sys
import traceback

try:
    print("Importing app...")
    from app import app, load_artifacts
    print("Import successful.")

    print("Loading artifacts...")
    load_artifacts()
    print("Artifacts loaded.")

except Exception:
    traceback.print_exc()
