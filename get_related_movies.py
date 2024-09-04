from get_movies import TMDBAPI
from dotenv import load_dotenv
import os
import requests

tmdb_api = TMDBAPI()

load_dotenv()

def get_related_movies(movie_id, language):
    api_url = os.getenv("TMDB_API_URL")
    api_token = os.getenv("TMDB_API_TOKEN")

    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None

    api_url += f"/movie/{movie_id}/recommendations?language={language}&page=1"

    headers = {"accept": "application/json", "Authorization": f"Bearer {api_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        results = response.json().get("results", [])
        formatted_results = []

        for movie in results:
            cast_and_crew = tmdb_api.get_movie_cast_n_crew(movie.get("id"))
            api_images_url = os.getenv("TMDB_IMAGES_API_URL")
            
            formatted_movie = {
                "id": movie.get("id") or None,
                "name": movie.get("title") or None,
                "year": int(movie.get("release_date", "0000-00-00").split("-")[0])
                or None,
                "poster": f"{api_images_url}{movie.get('poster_path', '')}"
                or None,
                "overview": movie.get("overview") or 'No overview available',
                "cast_and_crew": cast_and_crew,
                "popularity": movie.get("popularity") or None,
                "rating": movie.get("vote_average") or None,
            }

            genre_names = [
                tmdb_api.get_movie_genre(genre_id).get("name")
                for genre_id in movie.get("genre_ids", [])
                if tmdb_api.get_movie_genre(genre_id)
            ]

            formatted_movie["genre"] = ", ".join(genre_names)

            providers = tmdb_api.get_movie_watching_providers(movie.get("id"), "BR")

            if providers:
                formatted_movie["providers"] = providers

            formatted_results.append(formatted_movie)

        return formatted_results

    print("Error:", response.status_code, response.text)
    return None