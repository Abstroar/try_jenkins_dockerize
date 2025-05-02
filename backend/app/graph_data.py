# import yfinance as yf
# import pandas as pd
# from pymongo import MongoClient
#
# client = MongoClient("mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone")
# db = client["stock_database"]
#
#
# # , "MSFT", "GOOG", , "TSLA", "META", "NFLX", "NVDA"
# done = ["amzn", "aapl","MSFT","GOOG","TSLA", "NFLX","META"]
# def large_uploader():
#     STOCK_SYMBOLS = ["META"]
#     for symbol in STOCK_SYMBOLS:
#         print(f"Fetching data for {symbol}...")
#         collection = db[symbol.lower()]
#         data = yf.download(symbol, period='3y')  # Use 'max' for full history like your CSV
#         if data.empty:
#             print(f"No data found for {symbol}.")
#             continue
#
#         data.reset_index(inplace=True)
#         data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]  # Keep only necessary columns
#         data['Date'] = pd.to_datetime(data['Date'], format="%Y-%m-%d")  # Ensure datetime format
#
#         documents = data.to_dict(orient="records")
#
#         for i, doc in enumerate(documents):
#             documents[i] = {str(key): value for key, value in doc.items()}
#
#             # Insert the documents into the MongoDB collection
#         collection.insert_many(documents)
#         print(f"Uploaded {len(documents)} records for {symbol}.")
# large_uploader()
# print("hii")
#
# #
# # def upload_from_csv():
# #     collection = db["aapl"]
# #
# #     data = pd.read_csv("D:/Capstone project/another/backend/app/AAPL.csv")
# #     data['Date'] = pd.to_datetime(data['Date'], format="%Y-%m-%d")
# #
# #     data.reset_index(drop=True, inplace=True)
# #
# #     documents = data.to_dict(orient="records")
# #
# #     if documents:
# #         collection.insert_many(documents)
# #         print(f"Saved {len(documents)} records from CSV.")
# #     else:
# #         print("CSV file is empty!")
# #
# # upload_from_csv()
# print("done")