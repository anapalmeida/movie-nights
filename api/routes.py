from flask import jsonify, request
from get_matching_movies import get_matching_movies
from get_related_movies import get_related_movies
from dotenv import load_dotenv

import os

load_dotenv()

watchlist_1 = os.getenv("DATASET_WATCHLIST_1_PATHNAME")
watchlist_2 = os.getenv("DATASET_WATCHLIST_2_PATHNAME")

def configure_routes(app):
    @app.route('/api/matching_movies', methods=['GET'])
    def matching_movies():
        results = get_matching_movies(watchlist_1, watchlist_2)
        return jsonify(results)
    
    @app.route('/api/related_movies', methods=['GET'])
    def related_movies():
        results = get_related_movies('19', "en-US")
        return jsonify(results)

