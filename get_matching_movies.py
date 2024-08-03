from get_movies import TMDBAPI
from utils.generate_array_objects import generate_array_objects
from utils.generate_csv import generate_csv

tmdb_api = TMDBAPI()

def get_matching_movies(watchlist_1_pathname, watchlist_2_pathname):
    filteredMovies = tmdb_api.set_movie_info(watchlist_1_pathname, watchlist_2_pathname)
    generate_csv(filteredMovies, "matching_movies.csv")
    results = generate_array_objects("matching_movies.csv")

    return results
