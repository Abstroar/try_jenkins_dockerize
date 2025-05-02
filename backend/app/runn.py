import yfinance as yf
import tensorflow as tf
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def use_model(ticker: str):
    ticker = ticker.upper()
    model = load_model('./model_try/lstm_risk_model.keras')
    new_data = yf.download(ticker, period='6mo', interval='1d')
    close_prices = new_data['Close'].values
    close_prices = [float(x[0]) for x in close_prices]
    returns = np.diff(close_prices) / close_prices[:-1]
    window_size = 60
    volatility = np.array(
        [np.std(returns[i - window_size:i]) if i >= window_size else 0 for i in range(1, len(returns))])

    volatility = volatility[window_size - 1:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_volatility = scaler.fit_transform(volatility.reshape(-1, 1))
    x_input = []
    for i in range(window_size, len(scaled_volatility)):
        x_input.append(scaled_volatility[i - window_size:i, 0])
    x_input = np.array(x_input)
    x_input = np.reshape(x_input, (x_input.shape[0], x_input.shape[1], 1))

    predicted_risk = model.predict(x_input)
    predicted_risk_actual = scaler.inverse_transform(predicted_risk)
    result = predicted_risk_actual[0][0] + predicted_risk_actual[1][0]

    return result


# [[0.03198559]
#  [0.03202311]]
# x = use_model("aapl")
# print(x)
# model = tf.keras.Sequential([
#         tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(60, 1)),
#         tf.keras.layers.LSTM(64, return_sequences=False),
#         tf.keras.layers.Dense(25),
#         tf.keras.layers.Dense(1)
#     ])
#
# # model.compile(optimizer='adam', loss='mean_squared_error')
# model.save('./model_try/full_model.h5')
# model = tf.keras.models.load_model('./model_try/full_model.h5')
# model.load_weights('./model_try/model_.weights.h5', by_name=True)