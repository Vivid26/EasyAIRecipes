import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ollama_utils import generate_recipe
from db import get_collection, save_recipe, get_favorites

app = Flask(__name__)
CORS(app)

favorites_collection = get_collection()

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
        save_recipe(favorites_collection, data)
        return jsonify({"message": "Recipe saved to favorites!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/favorites', methods=['GET'])
def favorite_recipes():
    try:
        favorites = get_favorites(favorites_collection)
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
if __name__ == '__main__':
    app.run()
