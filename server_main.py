
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class APIKeys(BaseModel):
    api_key: str
    api_secret: str

@app.post("/set_keys")
async def set_keys(keys: APIKeys):
    print("✅ Received API keys:")
    print("Key:", keys.api_key)
    print("Secret:", keys.api_secret)
    return {"message": "Keys received successfully"}

@app.post("/trade")
async def start_trading():
    print("🚀 Trading started")
    return {"message": "AI Trading started"}

@app.post("/stop")
async def stop_trading():
    print("🛑 Trading stopped")
    return {"message": "Trading stopped"}
