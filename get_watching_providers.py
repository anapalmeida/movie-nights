from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_watching_providers(movie_id, locale):
    api_url = os.getenv('TMDB_API_URL')
    api_token = os.getenv('TMDB_API_TOKEN')
    
    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None
    
    api_url = f"{api_url}/movie/{movie_id}/watch/providers"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json().get('results', {}).get(locale, {})
    
    print("Error:", response.status_code, response.text)
    return None
