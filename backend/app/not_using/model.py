from pymongo import MongoClient
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["risk_db"]
collection = db["application_data"]

def train_regression_model():
    data = list(collection.find({}, {"_id": 0}))  # Fetch data, exclude MongoDB ID
    if len(data) < 2:
        return None  # Not enough data for regression
    
    df = pd.DataFrame(data)
    
    if "risk_score" not in df.columns:
        return None  # Target column missing

    X = df.drop(columns=["risk_score"])  # Features
    y = df["risk_score"]  # Target

    if X.empty or y.isnull().any():
        return None  # Ensure valid training data

    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_risk(input_data):
    model = train_regression_model()
    if not model:
        return None
    
    df = pd.DataFrame([input_data])
    
    # Ensure input columns match training features
    if set(df.columns) != set(model.feature_names_in_):
        return None
    
    prediction = model.predict(df)[0]
    return prediction
