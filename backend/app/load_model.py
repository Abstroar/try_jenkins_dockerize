import joblib
import os

# Create a 'models' directory if it doesn't exist
os.makedirs('models', exist_ok=True)

def load_model(filename='risk_model.pkl'):
    filepath = os.path.join('models', filename)
    return joblib.load(filepath)