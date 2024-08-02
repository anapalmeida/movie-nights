from flask import Flask, jsonify, request
from get_matching_movies import get_matching_movies
from get_related_movies import get_related_movies
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

watchlist_1 = os.getenv("DATASET_WATCHLIST_1_PATHNAME")
watchlist_2 = os.getenv("DATASET_WATCHLIST_2_PATHNAME")

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def configure_routes(app):
    @app.route('/api/upload_csv', methods=['POST'])
    def upload_csv():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
    
        file = request.files['file']
    
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
    
        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        
            try:
                df = pd.read_csv(file_path)
            
                required_columns = {'Date', 'Name', 'Year', 'Letterboxd URI'}
                if not required_columns.issubset(df.columns):
                    return jsonify({'error': 'CSV file is missing required columns'}), 400
        
                return jsonify({'message': 'File successfully uploaded and format validated'}), 200
            except Exception as e:
                return jsonify({'error': f'Error processing the CSV file: {e}'}), 500
        
        return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

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

configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
