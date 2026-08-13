
from pymongo import MongoClient

def get_documents():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["doc_assistant"]
    collection = db["documents"]
    return list(collection.find({"content": {"$exists": True}}))
