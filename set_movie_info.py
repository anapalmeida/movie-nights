import sys
import pandas as pd
import os
from get_movie_info import get_movie_info
from get_movie_genre import get_movie_genre
from get_watching_providers import get_watching_providers
from dotenv import load_dotenv
from utils.print_loading_screen import print_loading_animation

load_dotenv()


def set_movie_info():
    matching_movies = pd.read_csv("matching_movies.csv")
    api_images_url = os.getenv("TMDB_IMAGES_API_URL")

    matching_movies["ID"] = pd.NA
    matching_movies["Poster"] = pd.NA
    matching_movies["Overview"] = pd.NA
    matching_movies["Popularity"] = pd.NA
    matching_movies["Rating"] = pd.NA
    matching_movies["Genre"] = pd.NA
    matching_movies["Providers"] = pd.NA

    stop_event = print_loading_animation("Fetching movie data...")

    try:
        for index, row in matching_movies.iterrows():
            movie = get_movie_info(row["Year"], row["Name"])
            if movie:
                id = movie.get("id")
                poster = movie.get("poster_path")
                overview = movie.get("overview")
                popularity = movie.get("popularity")
                rating = movie.get("vote_average")
                genre = movie.get("genre_ids", [])
                genre_names = []

                matching_movies["Year"] = matching_movies["Year"].astype("Int64")

                if id:
                    matching_movies.at[index, "ID"] = id

                if poster:
                    matching_movies.at[index, "Poster"] = api_images_url + poster

                if overview:
                    matching_movies.at[index, "Overview"] = overview

                if popularity:
                    matching_movies.at[index, "Popularity"] = popularity

                if rating:
                    matching_movies.at[index, "Rating"] = rating

                if genre:
                    for genre_id in movie.get("genre_ids", []):
                        genre = get_movie_genre(genre_id)
                        if genre:
                            genre_names.append(genre.get("name"))
                        else:
                            print(f"Genre not found: {genre_id}")

                matching_movies.at[index, "Genre"] = ", ".join(genre_names)

                providers = get_watching_providers(id, "BR")
                if providers:
                    matching_movies.at[index, "Providers"] = providers

            else:
                print(f"Movie not found: {row['Name']} {row['Year']}")

    finally:
        stop_event.set()
        sys.stdout.write("\n")

    columns = [
        "ID",
        "Name",
        "Year",
        "Poster",
        "Overview",
        "Popularity",
        "Rating",
        "Genre",
        "Providers",
    ]
    matching_movies = matching_movies[columns]

    return matching_movies
