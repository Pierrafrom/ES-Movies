import json
import os

import requests
from flask import Blueprint, request, jsonify
from backend.config.constants import CACHE_PATH
from backend.models.python.User import User
from backend.services.data_formatter import get_data_as_lisp
from backend.services.movie_selector import call_expert_system
from backend.utils.api_key_manager import get_api_key

# Crée un Blueprint pour les routes API
api_bp = Blueprint('api', __name__)


@api_bp.route('/submit-movies', methods=['POST'])
def submit_movies():
    try:
        # Récupérer les données envoyées par le formulaire
        data = request.json
        print(f"Received data: {data}")  # Log les données reçues
        name = data.get("name")
        age = data.get("age")
        favorite_movies = data.get("favoriteMovies", [])
        mood_movies = data.get("moodMovies", [])

        print(f"Name: {name}, Age: {age}, Favorite Movies: {favorite_movies}, Mood Movies: {mood_movies}")

        # Appeler le système expert (simulez une réponse pour tester)
        user = User(name=name, age=age)
        user.set_favorite_movies(favorite_movies)
        user.set_mood_movies(mood_movies)

        lisp_data = get_data_as_lisp(CACHE_PATH, user)  # Conversion en Lisp
        json_response = call_expert_system(lisp_data)  # Appel au système expert
        print(f"Expert system response: {json_response}")

        return json_response  # Retourner la réponse du système expert
    except json.JSONDecodeError as json_error:
        print("JSON parsing failed:", json_error)
        return jsonify({"error": "JSON parsing failed", "details": str(json_error)}), 500

    except Exception as e:
        print("An unexpected error occurred:", e)
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@api_bp.route('/search-movie', methods=['GET'])
def search_movie():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": get_api_key(),
        "query": query
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        limited_results = data.get('results', [])[:5]
        return jsonify(limited_results)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
