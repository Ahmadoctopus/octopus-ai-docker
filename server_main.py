
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow all origins for global access (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_data = {}

@app.get("/")
def root():
    return {"message": "Server is running ✅"}

@app.post("/set_keys")
def set_keys(api_key: str = Form(...), api_secret: str = Form(...)):
    api_data["api_key"] = api_key
    api_data["api_secret"] = api_secret
    print("✅ Received API keys.")
    return {"status": "success", "message": "API keys received"}

@app.post("/trade")
def start_trading():
    if "api_key" not in api_data or "api_secret" not in api_data:
        return {"status": "error", "message": "API keys not set"}
    print("▶️ Starting AI trading...")
    return {"status": "success", "message": "AI trading started"}

@app.post("/stop")
def stop_trading():
    print("⛔ Trading stopped.")
    return {"status": "success", "message": "Trading stopped"}
