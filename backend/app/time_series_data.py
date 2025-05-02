from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class TimeSeriesDataService:
    def __init__(self,
                 db_uri: str = "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone",
                 db_name: str = 'stock_database'):
        try:
            self.client = MongoClient(
                db_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                retryWrites=True,
                retryReads=True,
                maxPoolSize=50,
                minPoolSize=10
            )
            self.db = self.client[db_name]
            self.collection = self.db["stock_collection"]
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def get_time_series_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
        """
        Fetch time series data for a given symbol from the database.
        If no dates are provided, returns the last 30 days of data.
        """
        try:
            # If no dates provided, default to last 30 days
            if not start_date or not end_date:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
            else:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")

            # Query the database
            query = {
                "symbol": symbol.upper(),
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }

            # Sort by date in ascending order
            cursor = self.collection.find(query).sort("date", 1)
            
            # Convert to list of dictionaries
            data = list(cursor)
            
            if not data:
                logger.warning(f"No data found for {symbol} between {start_date} and {end_date}")
                return []

            # Format the data
            formatted_data = []
            for item in data:
                formatted_data.append({
                    "date": item["date"],
                    "current_price": float(item["current_price"]),
                    "open_price": float(item["open_price"]),
                    "high_price": float(item["high_price"]),
                    "low_price": float(item["low_price"]),
                    "volume": int(item["volume"])
                })

            return formatted_data

        except Exception as e:
            logger.error(f"Error fetching time series data for {symbol}: {str(e)}")
            raise

    def get_latest_data(self, symbol: str) -> Optional[dict]:
        """
        Get the most recent data point for a given symbol
        """
        try:
            data = self.collection.find_one(
                {"symbol": symbol.upper()},
                sort=[("date", -1)]
            )
            
            if not data:
                return None
                
            return {
                "date": data["date"],
                "current_price": float(data["current_price"]),
                "open_price": float(data["open_price"]),
                "high_price": float(data["high_price"]),
                "low_price": float(data["low_price"]),
                "volume": int(data["volume"])
            }
            
        except Exception as e:
            logger.error(f"Error fetching latest data for {symbol}: {str(e)}")
            return None

    def get_available_symbols(self) -> List[str]:
        """
        Get a list of all available stock symbols in the database
        """
        try:
            symbols = self.collection.distinct("symbol")
            return sorted(symbols)
        except Exception as e:
            logger.error(f"Error fetching available symbols: {str(e)}")
            return [] 