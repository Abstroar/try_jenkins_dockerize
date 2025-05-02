import os
from datetime import datetime, timedelta
from pymongo import MongoClient
import requests
from dotenv import load_dotenv

# Load environment variables (e.g., API keys)
load_dotenv()

# Config
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_URL = "https://finnhub.io/api/v1/quote"
STOCKS = ["AAPL", "GOOGL", "MSFT"]  # Add more symbols as needed

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client.stock_db
collection = db.stock_prices

def fetch_stock_price(symbol: str) -> dict:
    """Fetch stock price from Finnhub API."""
    try:
        response = requests.get(
            FINNHUB_URL,
            params={"symbol": symbol, "token": FINNHUB_API_KEY}
        )
        response.raise_for_status()
        data = response.json()
        if "c" not in data:
            raise ValueError(f"No price data for {symbol}")
        return {
            "symbol": symbol,
            "value": data["c"],
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def update_stocks():
    """Update all stocks in the DB."""
    for symbol in STOCKS:
        data = fetch_stock_price(symbol)
        if data:
            collection.update_one(
                {"symbol": symbol},
                {"$set": data},
                upsert=True  # Insert if not exists
            )
            print(f"Updated {symbol} at {data['timestamp']}")

if __name__ == "__main__":
    update_stocks()  # Run manually or via scheduler