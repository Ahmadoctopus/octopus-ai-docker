
from fastapi import FastAPI, Request
from pydantic import BaseModel
from octopus_ai.model import AITrader
import os

app = FastAPI()

api_keys = {"api_key": None, "api_secret": None}
ai_trader = None

class APIKeys(BaseModel):
    api_key: str
    api_secret: str

@app.post("/set_keys")
def set_keys(keys: APIKeys):
    global ai_trader
    api_keys["api_key"] = keys.api_key
    api_keys["api_secret"] = keys.api_secret
    ai_trader = AITrader(keys.api_key, keys.api_secret)
    return {"message": "API keys received successfully"}

@app.get("/capital")
def get_capital():
    if not ai_trader:
        return {"capital": 0}
    capital = ai_trader.get_balance()
    return {"capital": capital}

@app.get("/open_trades")
def get_open_trades():
    if not ai_trader:
        return {"trades": []}
    trades = ai_trader.get_open_trades()
    return {"trades": trades}
import os
import ccxt
import pandas as pd
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from octopus_ai.model import DummyAIModel

load_dotenv()

app = FastAPI()

binance = None
ai_model = DummyAIModel()
is_trading = False

class APIKeys(BaseModel):
    api_key: str
    api_secret: str

@app.post("/set_keys")
async def set_keys(keys: APIKeys):
    global binance
    binance = ccxt.binance({
        "apiKey": keys.api_key,
        "secret": keys.api_secret,
        "enableRateLimit": True
    })
    try:
        balance = binance.fetch_balance()
        return {"message": "✅ API keys set successfully", "balance": balance['total']}
    except Exception as e:
        return {"error": f"❌ Failed to connect: {str(e)}"}

@app.post("/trade")
async def start_trading():
    global is_trading
    is_trading = True
    if not binance:
        return {"error": "❌ Binance client not initialized."}
    try:
        markets = binance.load_markets()
        symbol = "BTC/USDT"
        ohlcv = binance.fetch_ohlcv(symbol, timeframe='1m', limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        prediction = ai_model.predict(df)
        if prediction == "buy":
            order = binance.create_market_buy_order(symbol, 0.001)
            return {"message": "✅ Buy order executed", "order": order}
        elif prediction == "sell":
            order = binance.create_market_sell_order(symbol, 0.001)
            return {"message": "✅ Sell order executed", "order": order}
        else:
            return {"message": "⚠️ No action taken"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/stop")
async def stop_trading():
    global is_trading
    is_trading = False
    return {"message": "🛑 Trading stopped"}

@app.get("/")
async def root():
    return {"message": "Octopus AI Trading API is running"}
