from fastapi import FastAPI, HTTPException, Query, Request, Depends, status
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import os

import logging
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv


load_dotenv()


from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import logging
import ssl
import yfinance as yf
import time
# get stock data
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
            
            # if start > current_date:
            #     raise ValueError(f"Start date {start_date} is in the future. Please use a date up to today.")
            # if end > current_date:
            #     raise ValueError(f"End date {end_date} is in the future. Please use a date up to today.")
            
            # Get available date range
            earliest_date, latest_date = self.get_available_date_range(symbol)
            
            # If no data in database, try yfinance
            # if not earliest_date or not latest_date:
            #     logger.info(f"No data found in database for {symbol}, trying yfinance...")
            #     return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            
            # Check if requested dates are within available range
            # if start > latest_date:
            #     logger.info(f"Start date {start_date} is after latest available data, trying yfinance...")
            #     return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            # if end < earliest_date:
            #     logger.info(f"End date {end_date} is before earliest available data, trying yfinance...")
            #     return self.get_stock_data_from_yfinance(start_date, end_date, symbol)
            
            # Adjust dates to available range if needed
            # if start < earliest_date:
            #     start = earliest_date
            #     logger.info(f"Adjusted start date to earliest available: {start.strftime('%Y-%m-%d')}")
            # if end > latest_date:
            #     end = latest_date
            #     logger.info(f"Adjusted end date to latest available: {end.strftime('%Y-%m-%d')}")

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
        
## home_data
import yfinance as yf
from fastapi import HTTPException
import requests
from datetime import datetime

API_KEY = '7bf9b1f7bee44c049e1b4442e7bf278d'
def get__stock_data(symbol: str):
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from TwelveData")

    data = response.json()
    if "code" in data:  # TwelveData returns 'code' field if error
        raise HTTPException(status_code=404, detail="Stock not found")

    return {
        "symbol": data["symbol"],
        "current_price": data["close"],
        "open_price": data["open"],
        "high_price": data["high"],
        "low_price": data["low"],
        "volume": data.get("volume"),
        "date": datetime.now()
    }

from pymongo import MongoClient
from datetime import datetime
# from .stock_data import get_onday_data as get_stock_data # Import your function to fetch stock data
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


## stock data
import yfinance as yf
from fastapi import HTTPException
import requests
from datetime import datetime

API_KEY = '7bf9b1f7bee44c049e1b4442e7bf278d'
def get_onday_data(symbol: str):
    url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from TwelveData")

    data = response.json()
    if "code" in data:  # TwelveData returns 'code' field if error
        raise HTTPException(status_code=404, detail="Stock not found")

    return {
        "symbol": data["symbol"],
        "current_price": data["close"],
        "open_price": data["open"],
        "high_price": data["high"],
        "low_price": data["low"],
        "volume": data.get("volume"),
        "date": datetime.now()
    }



























# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS setup (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow both Vite and React default ports
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=3600,  # Cache preflight requests for 1 hour
)

# MongoDB setup with retry logic
def connect_to_mongodb(max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            client = MongoClient(
                "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone",
                ssl=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            # Test the connection
            client.admin.command('ping')
            print(f"Successfully connected to MongoDB on attempt {attempt + 1}!")
            return client
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to MongoDB.")
                raise

try:
    client = connect_to_mongodb()
    db = client["stock_database"]
    if "users" not in db.list_collection_names():
        db.create_collection("users")
    if "portfolios" not in db.list_collection_names():
        db.create_collection("portfolios")
    collection = db["stock_data"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise


FINNHUB_API_KEY = "d02p359r01qi6jgif6p0d02p359r01qi6jgif6pg"
FINNHUB_URL = "https://finnhub.io/api/v1/quote"


class StockData(BaseModel):
    symbol: str
    value: float
    timestamp: datetime


class StockDataResponse(BaseModel):
    date: str
    avg_close: float



@app.get("/stocks-graph", response_model=list[StockDataResponse])
def get_stock_data(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD"),
    symbol: str = Query(..., description="Stock tocken"),
    aggregate: Optional[str] = Query("monthly", description="Aggregate by 'monthly' or 'yearly'")):
    try:
        if aggregate not in ['daily', 'weekly', 'monthly', 'yearly']:
            raise HTTPException(
                status_code=400,
                detail="Invalid aggregate parameter. Must be one of: daily, weekly, monthly, yearly"
            )
        if not symbol.isalpha():
            raise HTTPException(
                status_code=400,
                detail="Invalid symbol format. Must contain only letters"
            )
            
        logger.info(f"Received request for {symbol} from {start_date} to {end_date} with aggregation {aggregate}")
        service = StockDataService()
        data = service.get_stock_data_from_db(start_date, end_date, symbol.lower(), aggregate)
        logger.info(f"Returning {len(data)} data points")
        return data
    except ValueError as e:
        logger.error(f"ValueError in get_stock_data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_stock_data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching stock data")


@app.get("/api/stocks")
def get_all_stocks():
    try:
        raw_data = get_all_stocks_data()
        cleaned = [clean_stock_data(stock) for stock in raw_data]
        return cleaned
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/risk-prediction/{symbol}")
async def get_risk_prediction(symbol: str):
    return "Mediam risk"



@app.get('/api/fetch-stock/{symbol}')
def fetch_stock(symbol):
    symbol = symbol.upper()
    try :
        x = get_onday_data(symbol)
        return {
            "symbol": x["symbol"],
            "current_price": x["current_price"],
            "open_price": x["open_price"],
            "high_price": x["high_price"],
            "low_price": x["low_price"],
            "volume": x["volume"],
            "date": x["date"]
        }
    except Exception as e:
        print(f"Error in fetch_stock: {str(e)}")
        return {"status": "error", "message": "Internal server error"}


# import tensorflow as tf
# import numpy as np
# # from alpha_vantage.timeseries import TimeSeries
# import pandas

@app.get('/risk/{symbol}')
def load_and_predict_with_current_price(symbol, model_path_dir="./", api_key="PKSARG796MUFC2RK"):
#     # lstm_model = tf.keras.models.load_model(f"lstm_model.h5")



#     # ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='date')
#     # data, _ = ts.get_intraday(symbol=symbol, interval='15min', outputsize='compact')
#     # data = data.rename(columns={'4. close': 'current_price'})
#     # data = data.sort_index()  


#     # prices = data['current_price'].dropna().values[-50:]
#     # if len(prices) < 50:
#     #     raise ValueError(f"Not enough data points for {symbol}. Need at least 50, got {len(prices)}")


#     # lstm_input = np.reshape(prices, (1, 50, 1))
#     # rf_input = prices.reshape(1, -1)

#     # lstm_prediction = float(lstm_model.predict(lstm_input)[0][0])

#     # actual_latest_price = float(prices[-1])

    return {34}
