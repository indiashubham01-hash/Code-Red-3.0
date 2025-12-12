from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI()

class ReportInput(BaseModel):
    prediction: Dict[str, Any]
    symptoms: List[str]

@app.post("/generate_report")
def report(input_data: ReportInput):
    return {"report": "Minimal works"}

class ChatInput(BaseModel):
    message: str

if __name__ == "__main__":
    print("Starting Minimal Server...")
    uvicorn.run(app, host="0.0.0.0", port=8004)
