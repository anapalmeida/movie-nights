import pandas as pd
import requests
import sys
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import cachetools

from utils.read_and_generate_csv import read_and_generate_csv

load_dotenv()

class TMDBAPI:
    def __init__(self):
        self.api_url = os.getenv("TMDB_API_URL")
        self.api_token = os.getenv("TMDB_API_TOKEN")
        self.api_images_url = os.getenv("TMDB_IMAGES_API_URL")
        self.cache = cachetools.LRUCache(maxsize=100)
        if not self.api_url or not self.api_token:
            print("API URL or Token not found in .env file")
            sys.exit()

    def _get(self, endpoint, params=None):
        url = f"{self.api_url}{endpoint}"
        headers = {"accept": "application/json", "Authorization": f"Bearer {self.api_token}"}
        cache_key = (url, frozenset(params.items()) if params else None)
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            self.cache[cache_key] = data
            return data
        print("Error:", response.status_code, response.text)
        return None

    def _batch_get_genres(self, genre_ids):
        response = self._get("/genre/movie/list", {"language": "en-US"})
        if not response:
            return {}
        
        genres = response.get("genres", [])
        genre_map = {genre["id"]: genre for genre in genres}
        return {genre_id: genre_map.get(genre_id) for genre_id in genre_ids}

    def get_movie_genre(self, genre_id):
        genres = self._batch_get_genres([genre_id])
        return genres.get(genre_id)

    def get_movie_watching_providers(self, movie_id, locale):
        response = self._get(f"/movie/{movie_id}/watch/providers")
        if response:
            return response.get("results", {}).get(locale, {})
        return None

    def get_movie_info(self, movie_year, movie_name):
        response = self._get(
            "/search/movie",
            {"query": movie_name, "include_adult": "false", "language": "en-US", "page": 1, "year": movie_year}
        )
        if response:
            results = response.get("results", [])
            if results:
                return results[0]
            print(f"Movie not found: {movie_name} {movie_year}")
        return None

    def get_movie_cast_n_crew(self, movie_id):
        response = self._get(f"/movie/{movie_id}/credits")
        if response:
            cast = response.get("cast")
            crew = response.get("crew")
            results = {
                "cast": cast,
                "director": [person for person in crew if person.get("job") == "Director"],
                "writer": [person for person in crew if person.get("job") == "Writer"],
            }
            return results
        return None

    def set_movie_info(self, watchlist_1_pathname, watchlist_2_pathname):
        read_and_generate_csv(watchlist_1_pathname, watchlist_2_pathname)
        matching_movies = pd.read_csv("matching_movies.csv")
        
        columns_to_initialize = [
            "ID", "Poster", "Overview", "Cast and Crew", "Popularity", "Rating", "Genre", "Providers",
        ]
        for column in columns_to_initialize:
            matching_movies[column] = pd.NA

        # Uncomment this line when you have the loading animation implemented
        # stop_event = print_loading_animation("Fetching and rearranging movies data...")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            for index, row in matching_movies.iterrows():
                movie_future = executor.submit(self.get_movie_info, row["Year"], row["Name"])
                futures[movie_future] = index

            for future in as_completed(futures):
                index = futures[future]
                movie = future.result()
                if not movie:
                    print(f"Movie not found: {matching_movies.at[index, 'Name']} {matching_movies.at[index, 'Year']}")
                    continue

                id = movie.get("id")
                poster = movie.get("poster_path")
                overview = movie.get("overview")
                cast_and_crew = self.get_movie_cast_n_crew(id)
                popularity = movie.get("popularity")
                rating = movie.get("vote_average")
                genre_ids = movie.get("genre_ids", [])

                genre_names = [
                    self.get_movie_genre(genre_id).get("name")
                    for genre_id in genre_ids
                    if self.get_movie_genre(genre_id)
                ]

                providers = self.get_movie_watching_providers(id, "BR") if id else None

                matching_movies.at[index, "ID"] = id
                matching_movies.at[index, "Poster"] = (
                    self.api_images_url + poster if poster else pd.NA
                )
                matching_movies.at[index, "Overview"] = overview
                matching_movies.at[index, "Cast and Crew"] = cast_and_crew
                matching_movies.at[index, "Popularity"] = popularity
                matching_movies.at[index, "Rating"] = rating
                matching_movies.at[index, "Genre"] = ", ".join(genre_names)
                matching_movies.at[index, "Providers"] = providers

        columns = [
            "ID", "Name", "Year", "Poster", "Overview", "Cast and Crew", "Popularity", "Rating", "Genre", "Providers",
        ]
        matching_movies = matching_movies[columns]

        return matching_movies
