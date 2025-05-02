from pymongo import MongoClient
from datetime import datetime
from .stock_data import get_onday_data as get_stock_data # Import your function to fetch stock data
# Import your API function
# from your_api_module import fetch_stock_data
import logging

logger = logging.getLogger(__name__)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone",
    ssl=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=10000,
    retryWrites=True,
    retryReads=True
)
db = client["stock_database"]
collection = db["stock_data"]

STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NFLX", "NVDA"]

def refresh_or_get_stock(symbol: str):
    today_date = datetime.now().date()

    stock = collection.find_one({"symbol": symbol.upper()})

    if stock:
        stored_date = stock["date"].date()

        if stored_date == today_date:
            # print(f"Data for {symbol} is already fresh.")
            return stock  # return the existing fresh stock
        else:
            # print(f"Updating data for {symbol} (outdated).")
            fresh_data = get_stock_data(symbol)
            collection.update_one(
                {"symbol": symbol},
                {"$set": fresh_data},
                upsert=True
            )
            return fresh_data  # return fresh data

    else:
        # print(f"No data found for {symbol}, fetching new data.")
        fresh_data = get_stock_data(symbol)
        collection.insert_one(fresh_data)
        return fresh_data

def get_all_stocks_data():
    all_data = []
    for symbol in STOCK_SYMBOLS:
        try:
            stock_data = refresh_or_get_stock(symbol)
            all_data.append(stock_data)
        except Exception as e:
            print(f"Failed to fetch/update {symbol}: {str(e)}")
    return all_data

def clean_stock_data(stock: dict) -> dict:
    return {
        "symbol": stock["symbol"],
        "current_price": stock["current_price"],
        "open_price": stock["open_price"],
        "high_price": stock["high_price"],
        "low_price": stock["low_price"],
        "volume": stock["volume"],
        "date": stock["date"].strftime("%Y-%m-%d")}
