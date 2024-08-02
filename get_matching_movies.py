from read_and_generate_csv import read_and_generate_csv
from set_movie_info import set_movie_info
from generate_array_objects import generate_array_objects
from generate_csv import generate_csv


def get_matching_movies(watchlist_1_pathname, watchlist_2_pathname):
    read_and_generate_csv(watchlist_1_pathname, watchlist_2_pathname)
    populatedMovies = set_movie_info()
    generate_csv(populatedMovies, "matching_movies.csv")
    results = generate_array_objects("matching_movies.csv")

    return results
