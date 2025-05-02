from fastapi import FastAPI, HTTPException, Query, Request, Depends, status
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import os
import time
import logging
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from .get_stock_data import StockDataResponse, StockDataService
from .home_data import *
from dotenv import load_dotenv
from .stock_fetcher import fetch_and_store_stock_data
from .stock_data import get_onday_data as get_twelvedata_stock_data
from .time_series_data import TimeSeriesDataService
from .risk_prediction import RiskPredictionService
from .stock_data import get_onday_data

load_dotenv()

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
    time_series_service = TimeSeriesDataService()
    risk_prediction_service = RiskPredictionService()
    try:
        # Get time series data for the last 90 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        time_series_data = time_series_service.get_time_series_data(
            symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        if not time_series_data:
            return {
                "status": "error",
                "message": "Not enough historical data for risk prediction"
            }
        
        # Get risk prediction
        risk_prediction = risk_prediction_service.predict_risk(time_series_data)
        
        return {
            "status": "success",
            "data": risk_prediction
        }
        
    except Exception as e:
        print(f"Error in get_risk_prediction: {str(e)}")
        return {"status": "error", "message": "Internal server error"}


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





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)