from dotenv import load_dotenv

import os
import requests

load_dotenv()

def get_movie_genre(genre_id):
    api_url = os.getenv('TMDB_API_URL')
    api_token = os.getenv('TMDB_API_TOKEN')
  
    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None

    api_url += f"/genre/movie/list?api_key={api_token}&language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        genres = response.json().get('genres', [])
        for genre in genres:
            if genre['id'] == genre_id:
                return genre
        print(f"Genre with ID {genre_id} not found")
        return None
    
    print("Error:", response.status_code, response.text)
    return None
