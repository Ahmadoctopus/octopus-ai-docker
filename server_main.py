
import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from octopus_ai.trainer import start_ai_trading

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

@app.post("/set_keys")
async def set_keys(api_key: str = Form(...), api_secret: str = Form(...)):
    global BINANCE_API_KEY, BINANCE_API_SECRET
    BINANCE_API_KEY = api_key
    BINANCE_API_SECRET = api_secret
    return {"message": "✅ Keys updated"}

@app.post("/trade")
async def trade():
    result = start_ai_trading(BINANCE_API_KEY, BINANCE_API_SECRET)
    return {"message": result}

@app.post("/stop")
async def stop():
    return {"message": "🛑 Trading stopped (simulated)"}
