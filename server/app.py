from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from ollama_utils import generate_recipe

from flask import send_from_directory


app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ai_recipes"]
favorites_collection = db["favorites"]

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    ingredients = data.get("ingredients", "")
    recipe = generate_recipe(ingredients)
    return jsonify(recipe)

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    try:
        favorites_collection.insert_one(data)
        return jsonify({"message": "Recipe saved to favorites!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    try:
        favorites = list(favorites_collection.find({}, {'_id': 0}))  # Exclude MongoDB’s default _id
        return jsonify(favorites), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Serve React static files (after all API routes)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    static_folder = os.path.join(app.root_path, 'static')
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')

# Comment out for production WSGI servers like gunicorn
# if __name__ == '__main__':
#     app.run()
