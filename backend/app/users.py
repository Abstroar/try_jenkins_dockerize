from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import bcrypt

from pymongo.mongo_client import MongoClient


MONGO_URL = "mongodb+srv://abhilaksh:DVH1RDrl4DBUTCaA@capstone.vwbejki.mongodb.net/?retryWrites=true&w=majority&appName=Capstone"
client = MongoClient(MONGO_URL)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client['stock_database']
users_collection = db['users']



users_collection.create_index("username", unique=True)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)



def register_user(username: str, password: str, age: int, gender: str, profile_img: str) -> bool:
    try:
        user_data = {
            "username": username,
            "password": hash_password(password),
            "age": age,
            "gender": gender,
            "profile_img": profile_img,
            "portfolio": [] 
        }
        users_collection.insert_one(user_data)
        return True
    except DuplicateKeyError:
        return False

def login_user(username: str, password: str) -> bool:
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return True

def add_stock_to_portfolio(username: str, stock: str) -> bool:
    result = users_collection.update_one(
        {"username": username},
        {"$addToSet": {"portfolio": stock}} 
    )
    return result.modified_count > 0

def remove_stock_from_portfolio(username: str, stock: str) -> bool:
    result = users_collection.update_one(
        {"username": username},
        {"$pull": {"portfolio": stock}}  # Removes the stock if it exists
    )
    return result.modified_count > 0