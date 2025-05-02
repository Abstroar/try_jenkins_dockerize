import numpy as np
import pandas as pd
import joblib
import tensorflow
from tensorflow.keras.models import load_model
from alpha_vantage.timeseries import TimeSeries
import os


api_key = 'YOUR_NEW_API_KEY_HERE'


ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='date')


lstm_model = load_model('lstm_model.h5')
rf_model = joblib.load('rf_model.pkl')

print("✅ Models loaded successfully!")


def fetch_latest_stock_data(symbol):
    print(f"\n📦 Fetching latest data for {symbol}...")
    data, _ = ts.get_intraday(symbol=symbol, interval='15min', outputsize='full')
    data = data.rename(columns={
        '1. open': '1. open',
        '2. high': '2. high',
        '3. low': '3. low',
        '4. close': '4. close',
        '5. volume': '5. volume'
    })
    closing_prices = data['4. close'].values
    return closing_prices


def predict_next_price(symbol):
    prices = fetch_latest_stock_data(symbol)

    if len(prices) < 50:
        print(f"❌ Not enough data to predict for {symbol}. Need at least 50 data points.")
        return

    last_50_prices = prices[-50:]

    lstm_input = np.reshape(last_50_prices, (1, 50, 1))
    rf_input = np.reshape(last_50_prices, (1, 50))


    lstm_pred = lstm_model.predict(lstm_input)[0][0]
    rf_pred = rf_model.predict(rf_input)[0]

    print(f"\n📈 Predicted Next Price for {symbol}:")
    print(f"- LSTM Prediction: ${lstm_pred:.2f}")
    print(f"- Random Forest Prediction: ${rf_pred:.2f}")

predict_next_price('AAPL')  

print("\n✅ Prediction complete!")
