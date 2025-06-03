from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()  # Loads variables from .env into environment

MONGO_URI = os.getenv("MONGO_URI")

def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client["recipeDB"]
    return db["recipes"]

def save_recipe(collection, recipe):
    collection.insert_one(recipe)

def get_favorites(collection):
    return list(collection.find({}, {"_id": 0}))
