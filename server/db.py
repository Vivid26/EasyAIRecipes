import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env into environment

MONGO_URI = os.getenv("MONGO_URI")

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client["ai_recipes"]
    return db["favorites"]

def save_recipe(collection, recipe):
    collection.insert_one(recipe)

def get_favorites(collection):
    return list(collection.find({}, {"_id": 0}))
