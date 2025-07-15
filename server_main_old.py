
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class Keys(BaseModel):
    api_key: str
    api_secret: str

@app.post("/set_keys")
def set_keys(keys: Keys):
    os.environ["API_KEY"] = keys.api_key
    os.environ["API_SECRET"] = keys.api_secret
    return {"message": "✅ API keys set successfully."}

@app.post("/trade")
def start_trading():
    return {"message": "✅ AI trading started."}

@app.post("/stop")
def stop_trading():
    return {"message": "🛑 Trading stopped."}
