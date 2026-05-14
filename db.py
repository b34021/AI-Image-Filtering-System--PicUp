from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

def get_collection(collection_name):
    return db[collection_name]