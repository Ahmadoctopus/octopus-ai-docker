
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ccxt
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# CORS for development/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize variables
exchange = None
open_trades = []

class APIKeys(BaseModel):
    api_key: str
    api_secret: str

@app.post("/set_keys")
async def set_keys(keys: APIKeys):
    global exchange
    try:
        exchange = ccxt.binance({
            'apiKey': keys.api_key,
            'secret': keys.api_secret,
            'enableRateLimit': True
        })
        # Try fetch balance to validate keys
        balance = exchange.fetch_balance()
        return {"message": "API keys received and validated."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/capital")
async def get_capital():
    global exchange
    if not exchange:
        raise HTTPException(status_code=400, detail="API keys not set.")
    try:
        balance = exchange.fetch_balance()
        return {"capital": balance['total']['USDT']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/open_trades")
async def get_open_trades():
    global exchange
    if not exchange:
        raise HTTPException(status_code=400, detail="API keys not set.")
    try:
        orders = exchange.fetch_open_orders()
        return {"trades": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
