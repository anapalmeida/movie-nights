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
        try:
            results = get_matching_movies(watchlist_1, watchlist_2)
            return jsonify(results)
        except Exception as e:
            print(f"Error occurred: {e}")
            return jsonify({'error': 'An error occurred while fetching matching movies.'}), 500

    @app.route('/api/related_movies', methods=['GET'])
    def related_movies():
        try:
            movie_id = request.args.get('movie_id')
            language = request.args.get('language', default='en-US')
            
            if not movie_id:
                return jsonify({'error': 'Missing required parameter: movie_id'}), 400
            
            if not isinstance(movie_id, str) or not isinstance(language, str):
                return jsonify({'error': 'Invalid parameter types'}), 400

            results = get_related_movies(movie_id, language)
            return jsonify(results)
        except Exception as e:
            print(f"Error occurred: {e}")
            return jsonify({'error': 'An error occurred while fetching related movies.'}), 500
