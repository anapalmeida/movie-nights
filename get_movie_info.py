from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_movie_info(movie_year, movie_name):
    api_url = os.getenv('TMDB_API_URL')
    api_token = os.getenv('TMDB_API_TOKEN')
    
    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None

    api_url += f"/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1&year={movie_year}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json().get('results')[0]
        
    
    print("Error:", response.status_code, response.text)
    return None


