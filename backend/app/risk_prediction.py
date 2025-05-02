import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
import logging
from sklearn.preprocessing import MinMaxScaler
import os

logger = logging.getLogger(__name__)

class RiskPredictionService:
    def __init__(self, model_path='model_try/lstm_risk_model.h5'):
        try:
            # Get the absolute path to the model
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_abs_path = os.path.join(current_dir, model_path)
            
            if not os.path.exists(model_abs_path):
                raise FileNotFoundError(f"Model file not found at: {model_abs_path}")
                
            self.model = load_model(model_abs_path)
            logger.info(f"Successfully loaded LSTM risk prediction model from {model_abs_path}")
        except Exception as e:
            logger.error(f"Failed to load LSTM risk prediction model: {str(e)}")
            raise

    def prepare_data(self, time_series_data):
        """Prepare time series data for the LSTM model exactly as it was trained"""
        try:
            # Convert to DataFrame and get returns
            df = pd.DataFrame(time_series_data)
            returns = df['current_price'].pct_change().dropna().values
            
            # Calculate volatility with window_size=60
            window_size = 60
            volatility = np.array(
                [np.std(returns[i - window_size:i]) if i >= window_size else 0 
                 for i in range(1, len(returns))]
            )
            
            # Normalize volatility using MinMaxScaler
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_volatility = scaler.fit_transform(volatility.reshape(-1, 1))
            
            # Prepare input data exactly as in training
            x = []
            for i in range(window_size, len(scaled_volatility)):
                x.append(scaled_volatility[i - window_size:i, 0])
            
            x = np.array(x)
            x = np.reshape(x, (x.shape[0], x.shape[1], 1))
            
            return x
            
        except Exception as e:
            logger.error(f"Error preparing data for risk prediction: {str(e)}")
            raise

    def predict_risk(self, time_series_data):
        """Predict risk level based on time series data using LSTM model"""
        try:
            # Prepare data
            x = self.prepare_data(time_series_data)
            
            # Make prediction
            prediction = self.model.predict(x)
            
            # Get the latest prediction
            latest_prediction = prediction[-1][0]
            
            # Convert to risk level (0-100)
            risk_level = int(latest_prediction * 100)
            
            # Determine risk category
            if risk_level < 30:
                risk_category = "Low"
            elif risk_level < 70:
                risk_category = "Medium"
            else:
                risk_category = "High"
            
            return {
                "risk_level": risk_level,
                "risk_category": risk_category,
                "confidence": float(prediction[-1][0]),
                "model_type": "LSTM"
            }
            
        except Exception as e:
            logger.error(f"Error predicting risk: {str(e)}")
            raise

RiskPredictionService()