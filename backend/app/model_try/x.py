import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'META', 'NFLX', 'AMD', 'IBM']
all_data = []
for ticker in stocks:
    data = yf.download(ticker, period='5y', interval='1d')
    if not data.empty:
        all_data.append(data['Close'].values)
    else:
        print(f"Warning: No data for {ticker}")

# Check the shape of all_data and combined_data
print(f"Total number of stock data arrays: {len(all_data)}")
combined_data = np.concatenate(all_data)

flat_data = combined_data.flatten()
returns = np.diff(flat_data) / flat_data[:-1]

# Check if combined_data has values
if combined_data.size == 0:
    print("Error: No stock data combined.")
else:
    print(f"Combined data size: {combined_data.shape}")

    # Calculate rolling volatility (risk) over a window of 60 days
    window_size = 60
    volatility = np.array(
        [np.std(returns[i - window_size:i]) if i >= window_size else 0 for i in range(1, len(returns))])

    # Preprocess Data (Normalize risk values)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_volatility = scaler.fit_transform(volatility.reshape(-1, 1))

    # Prepare Training Data
    x_train, y_train = [], []
    for i in range(window_size, len(scaled_volatility)):
        x_train.append(scaled_volatility[i - window_size:i, 0])
        y_train.append(scaled_volatility[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Build and Train Model
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(window_size, 1)),
        tf.keras.layers.LSTM(64, return_sequences=False),
        tf.keras.layers.Dense(25),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=20, batch_size=32)


    model.save('./lstm_risk_model.h5')
    model.save('./lstm_risk_model.keras')



