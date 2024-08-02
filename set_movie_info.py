import sys
import pandas as pd
import os
from get_movie_info import get_movie_info
from get_movie_genre import get_movie_genre
from get_watching_providers import get_watching_providers
from get_cast_n_crew import get_cast_n_crew
from dotenv import load_dotenv
from utils.print_loading_screen import print_loading_animation

load_dotenv()

def set_movie_info():
    matching_movies = pd.read_csv("matching_movies.csv")
    api_images_url = os.getenv("TMDB_IMAGES_API_URL")

    columns_to_initialize = ["ID", "Poster", "Overview", "Popularity", "Rating", "Genre", "Providers"]
    for column in columns_to_initialize:
        matching_movies[column] = pd.NA

    stop_event = print_loading_animation("Fetching movie data...")

    try:
        for index, row in matching_movies.iterrows():
            movie = get_movie_info(row["Year"], row["Name"])
            if not movie:
                print(f"Movie not found: {row['Name']} {row['Year']}")
                continue
            
            id = movie.get("id")
            poster = movie.get("poster_path")
            overview = movie.get("overview")
            cast_and_crew = get_cast_n_crew(id)
            popularity = movie.get("popularity")
            rating = movie.get("vote_average")
            genre_ids = movie.get("genre_ids", [])

            genre_names = [
                get_movie_genre(genre_id).get("name")
                for genre_id in genre_ids
                if get_movie_genre(genre_id)
            ]

            providers = get_watching_providers(id, "BR") if id else None

            matching_movies.at[index, "ID"] = id
            matching_movies.at[index, "Poster"] = api_images_url + poster if poster else pd.NA
            matching_movies.at[index, "Overview"] = overview
            matching_movies.at[index, "Cast"] = cast_and_crew
            matching_movies.at[index, "Popularity"] = popularity
            matching_movies.at[index, "Rating"] = rating
            matching_movies.at[index, "Genre"] = ", ".join(genre_names)
            matching_movies.at[index, "Providers"] = providers

    finally:
        stop_event.set()
        sys.stdout.write("\n")

    columns = ["ID", "Name", "Year", "Poster", "Overview", "Cast", "Popularity", "Rating", "Genre", "Providers"]
    matching_movies = matching_movies[columns]

    return matching_movies
