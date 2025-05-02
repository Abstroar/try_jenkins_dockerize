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

# stock_data = get_stock_data('AAPL')
# print(stock_data)