from read_and_generate_csv import read_and_generate_csv
from set_movie_info import set_movie_info
from generate_array_objects import generate_array_objects
from generate_csv import generate_csv

def get_matching_movies():
  read_and_generate_csv()
  unsetMovies = set_movie_info()
  generate_csv(unsetMovies, 'matching_movies.csv')
  generate_array_objects('matching_movies.csv', 'matching_movies.json')