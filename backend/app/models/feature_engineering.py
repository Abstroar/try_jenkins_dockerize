import numpy as np
import pandas as pd

def add_features(df):
    """
    Add technical indicators as features for the model, without using pandas_ta.
    """
    # Daily Return
    df['Daily Return'] = df['Close'].pct_change()

    # Volatility (21-day rolling standard deviation of daily returns)
    df['Volatility'] = df['Daily Return'].rolling(window=21).std() * np.sqrt(252)

    # Moving Averages
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()

    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14, min_periods=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD (Moving Average Convergence Divergence)
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2

    # Bollinger Bands
    sma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    df['BB_upper'] = sma20 + (2 * std20)
    df['BB_middle'] = sma20
    df['BB_lower'] = sma20 - (2 * std20)

    # Drop any NaN values created
    df = df.dropna()

    return df
