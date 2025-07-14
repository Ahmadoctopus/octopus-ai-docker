
from .model import load_lstm_model
from .utils import analyze_market

def start_ai_trading(api_key, api_secret):
    model = load_lstm_model()
    market_info = analyze_market()
    return f"🤖 AI Trading started using {model} and {market_info} with API key {api_key[:4]}***"
