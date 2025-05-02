import numpy as np

"""
    Label the risk level based on volatility quantiles.
    Args:
        df (pd.DataFrame): Stock data with computed volatility.
    Returns:
        pd.DataFrame: Stock data with labeled risk levels.
"""
def label_risk(df):
    try:
        # Make sure 'Volatility' has no NaNs
        df = df.dropna(subset=['Volatility'])
        
        # Calculate quantiles
        quantiles = df['Volatility'].quantile([0.33, 0.66])
        
        # Define conditions and choices
        conditions = [
            (df['Volatility'] > quantiles[0.66]),
            (df['Volatility'] <= quantiles[0.66]) & (df['Volatility'] > quantiles[0.33]),
            (df['Volatility'] <= quantiles[0.33])
        ]
        choices = ['High', 'Medium', 'Low']
        
        # Apply labels
        df['Risk Level'] = np.select(conditions, choices, default='Unknown')
        
        return df
    except Exception as e:
        import traceback
        import logging
        logging.error(traceback.format_exc())
        raise ValueError(f"Error during labeling: {e}")
