import yfinance as yf
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional

# MongoDB connection
client = MongoClient(
    "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone",
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=10000,
    retryWrites=True,
    retryReads=True
)
db = client["stock_database"]
collection = db["stock_history"]

def fetch_and_store_stock_data(symbol: str, period: str = "1y", interval: str = "1d") -> Dict:
    """
    Fetch stock data from Yahoo Finance and store it in MongoDB.
    Returns the fetched data as a dictionary.
    """
    try:
        # Fetch data from Yahoo Finance
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        
        if hist.empty:
            raise ValueError(f"No data found for ticker: {symbol}")
        
        # Convert DataFrame to list of dictionaries
        data_list = []
        for index, row in hist.iterrows():
            data_point = {
                "symbol": symbol.upper(),
                "date": index.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
                "timestamp": datetime.now()
            }
            data_list.append(data_point)
        
        # Store in MongoDB
        if data_list:
            # Delete existing data for this symbol
            collection.delete_many({"symbol": symbol.upper()})
            # Insert new data
            collection.insert_many(data_list)
        
        return {
            "symbol": symbol.upper(),
            "data": data_list,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        raise ValueError(f"Error fetching/storing data for {symbol}: {str(e)}")

def get_stock_data(symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
    """
    Get stock data from MongoDB, fetching from Yahoo Finance if not available.
    """
    try:
        # Check if we have data in MongoDB
        query = {"symbol": symbol.upper()}
        if start_date and end_date:
            query["date"] = {
                "$gte": start_date,
                "$lte": end_date
            }
        
        data = list(collection.find(query, {"_id": 0}).sort("date", 1))
        
        if not data:
            # If no data found, fetch from Yahoo Finance
            fetch_and_store_stock_data(symbol)
            data = list(collection.find(query, {"_id": 0}).sort("date", 1))
        
        return data
        
    except Exception as e:
        raise ValueError(f"Error getting data for {symbol}: {str(e)}") 