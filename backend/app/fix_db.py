# from pymongo import MongoClient
#
# client = MongoClient("mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone")
# collection = client['stock_database']["META"]
#
# for doc in collection.find():
#     new_doc = {
#         "Date": doc.get("('Date', '')"),
#         "Open": doc.get("('Open', 'AMZN')"),
#         "High": doc.get("('High', 'AMZN')"),
#         "Low": doc.get("('Low', 'AMZN')"),
#         "Close": doc.get("('Close', 'AMZN')"),
#         "Volume": doc.get("('Volume', 'AMZN')")
#     }
#     collection.update_one({'_id': doc['_id']}, {'$set': new_doc})