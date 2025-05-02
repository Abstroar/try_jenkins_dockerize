# from .stock_data import get_stock_data
# import logging
# from pymongo import MongoClient
#
# logger = logging.getLogger(__name__)
#
# # Connect to MongoDB
# client = MongoClient(
#     "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone",
#     ssl=True,
#     tlsAllowInvalidCertificates=True,
#     serverSelectionTimeoutMS=5000,
#     connectTimeoutMS=10000,
#     socketTimeoutMS=10000,
#     retryWrites=True,
#     retryReads=True
# )
# db = client["stock_database"]
# collection = db["stock_data"]
#
#
# def function