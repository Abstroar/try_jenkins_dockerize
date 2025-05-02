from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import logging
import ssl
import yfinance as yf
import time

logger = logging.getLogger(__name__)

class StockDataResponse(BaseModel):
    date: str
    avg_close: float


class StockDataService:
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
            self.collection = self.db["stock_data"]
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def get_available_date_range(self, symbol: str) -> tuple:
        """Get the earliest and latest dates available for a symbol"""
        try:
            collection_name = symbol.lower()
            collection = self.db[collection_name]
            
            earliest = collection.find_one(
                {},
                sort=[("Date", 1)]
            )
            latest = collection.find_one(
                {},
                sort=[("Date", -1)]
            )
            
            if not earliest or not latest:
                return None, None
                
            return earliest["Date"], latest["Date"]
        except Exception as e:
            logger.error(f"Error getting date range for {symbol}: {str(e)}")
            return None, None

    def get_stock_data_from_db(self, start_date: str, end_date: str, symbol: str, aggregate: str = 'monthly') -> List[dict]:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            current_date = datetime.now()
            
            if start > current_date:
                raise ValueError(f"Start date {start_date} is in the future. Please use a date up to today.")
            if end > current_date:
                raise ValueError(f"End date {end_date} is in the future. Please use a date up to today.")
            
            # Get available date range
            earliest_date, latest_date = self.get_available_date_range(symbol)
            
            # If no data in database, try yfinance
            if not earliest_date or not latest_date:
                logger.info(f"No data found in database for {symbol}, trying yfinance...")
                return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            
            # Check if requested dates are within available range
            if start > latest_date:
                logger.info(f"Start date {start_date} is after latest available data, trying yfinance...")
                return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            if end < earliest_date:
                logger.info(f"End date {end_date} is before earliest available data, trying yfinance...")
                return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            
            # Adjust dates to available range if needed
            if start < earliest_date:
                start = earliest_date
                logger.info(f"Adjusted start date to earliest available: {start.strftime('%Y-%m-%d')}")
            if end > latest_date:
                end = latest_date
                logger.info(f"Adjusted end date to latest available: {end.strftime('%Y-%m-%d')}")

            collection_name = symbol.lower()
            collection = self.db[collection_name]

            data_list = list(collection.find({
                'Date': {'$gte': start, '$lte': end}
            }))

            if not data_list:
                raise ValueError(f"No data found for {symbol} between {start.strftime('%Y-%m-%d')} and {end.strftime('%Y-%m-%d')}")

            data = pd.DataFrame(data_list)

            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])

            if 'Close' not in data.columns:
                raise ValueError(f"Missing 'Close' field in data for {symbol}")

            if aggregate == 'daily':
                data['Day'] = data['Date'].dt.date
                aggregated_data = data.groupby('Day').agg({'Close': 'mean'}).reset_index()
                aggregated_data['Day'] = aggregated_data['Day'].astype(str)
                result = [{"date": row['Day'], "avg_close": row['Close']} for _, row in aggregated_data.iterrows()]

            elif aggregate == 'weekly':
                # Use ISO week for consistent weekly aggregation
                data['Week'] = data['Date'].dt.isocalendar().week.astype(int)  # Convert to integer
                data['Year'] = data['Date'].dt.year
                aggregated_data = data.groupby(['Year', 'Week']).agg({'Close': 'mean'}).reset_index()
                # Convert to YYYY-MM-DD format (using Monday of each week)
                aggregated_data['date'] = aggregated_data.apply(
                    lambda row: datetime.fromisocalendar(int(row['Year']), int(row['Week']), 1).strftime('%Y-%m-%d'),
                    axis=1
                )
                result = [{"date": row['date'], "avg_close": row['Close']} for _, row in aggregated_data.iterrows()]

            elif aggregate == 'monthly':
                data['Month'] = data['Date'].dt.to_period('M')
                aggregated_data = data.groupby('Month').agg({'Close': 'mean'}).reset_index()
                aggregated_data['Month'] = aggregated_data['Month'].astype(str)
                result = [{"date": row['Month'], "avg_close": row['Close']} for _, row in aggregated_data.iterrows()]

            elif aggregate == 'yearly':
                data['Year'] = data['Date'].dt.year
                aggregated_data = data.groupby('Year').agg({'Close': 'mean'}).reset_index()
                result = [{"date": str(row['Year']), "avg_close": row['Close']} for _, row in aggregated_data.iterrows()]

            else:
                raise ValueError("Invalid aggregate parameter. Choose from 'daily', 'weekly', 'monthly', or 'yearly'.")

            return result
        except ValueError as e:
            raise
        except Exception as e:
            logger.error(f"Error processing stock data: {str(e)}")
            raise ValueError(f"Error processing stock data: {str(e)}")

    # print("hello")
    # x = StockDataService().get_stock_data_from_db("2023-01-01", "2023-12-31","amzn",aggregate="daily")
    # print(x)