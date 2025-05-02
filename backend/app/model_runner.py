import numpy as np
import pandas as pd
import joblib
import tensorflow
from tensorflow.keras.models import load_model
from alpha_vantage.timeseries import TimeSeries
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, LSTM, Dense

# api_key = '3PDWBSV8VU44ZC0J'
api_key = '3PDWBSV8VU4dssd'

ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='date')


# lstm_model = load_model('lstm_model.h5')
rf_model = joblib.load('not_using/rf_model.pkl')




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
        return

    last_50_prices = prices[-50:]


    rf_input = np.reshape(last_50_prices, (1, 50))
    rf_pred = rf_model.predict(rf_input)[0]

    print(f"\n📈 Predicted Next Price for {symbol}:")
    # print(f"- LSTM Prediction: ${lstm_pred:.2f}")
    print(f"- Random Forest Prediction: ${rf_pred:.2f}")

predict_next_price('AAPL')

print("\n✅ Prediction complete!")