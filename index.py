from dotenv import load_dotenv

import os

load_dotenv()

from get_matching_movies import get_matching_movies
from get_related_movies import get_related_movies

watchlist_1 = os.getenv("DATASET_WATCHLIST_1_PATHNAME")
watchlist_2 = os.getenv("DATASET_WATCHLIST_2_PATHNAME")

bar = get_matching_movies(watchlist_1, watchlist_2)
print(bar)
foo = get_related_movies('19', "en-US")
