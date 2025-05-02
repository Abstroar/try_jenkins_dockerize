from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
from app.models.load_model import load_model
from app.models.labeling import label_risk
from app.models.data_collection import get_stock_data
from app.models.data_preprocessing import preprocess_data
from app.models.feature_engineering import add_features

def analyze_api(ticker):
    try:
        # Get stock data and analyze
        data = get_stock_data(ticker.upper())
        data = preprocess_data(data)
        data = add_features(data)
        data = label_risk(data)
        
        # Load the model
        model = load_model()
        
        # Get features for prediction
        features = ['Daily Return', 'Volatility', 'MA50', 'MA200']
        latest_data = data[features].iloc[-1]
        
        # Make prediction
        risk_level = model.predict(latest_data.values.reshape(1, -1))[0]
        
        # Prepare API response
        response = {
            'ticker': ticker.upper(),
            'analysis': {
                'risk_level': int(risk_level),
                'current_price': float(data['Close'].iloc[-1]),
                'volatility': float(data['Volatility'].iloc[-1]),
                'daily_return': float(data['Daily Return'].iloc[-1]),
                'last_updated': data.index[-1].isoformat()
            },
            'historical_data': {
                'dates': [d.isoformat() for d in data.index[-30:]],
                'prices': [float(p) for p in data['Close'].tail(30)]
            }
        }
        
        return response
    except Exception as e:
        import traceback
        import logging
        logging.error(traceback.format_exc())  # Log the full error on the server
        return {
            'error': 'An internal error has occurred.',
            'ticker': ticker.upper()
        }, 400

analyze_api('AAPL')