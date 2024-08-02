from dotenv import load_dotenv
import os
import requests

load_dotenv()


def get_related_movies(movie_id, locale):
    api_url = os.getenv("TMDB_API_URL")
    api_token = os.getenv("TMDB_API_TOKEN")

    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None

    api_url += f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?language={locale}&page=1"

    headers = {"accept": "application/json", "Authorization": f"Bearer {api_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json().get("results")[0]

    print("Error:", response.status_code, response.text)
    return None
