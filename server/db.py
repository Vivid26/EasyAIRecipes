from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["recipeDB"]
    return db["recipes"]

def save_recipe(collection, recipe):
    collection.insert_one(recipe)

def get_favorites(collection):
    return list(collection.find({}, {"_id": 0}))
