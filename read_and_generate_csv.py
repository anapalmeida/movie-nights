import pandas as pd
import os

from generate_csv import generate_csv
from dotenv import load_dotenv

load_dotenv()


def read_and_generate_csv():

    df1 = pd.read_csv(os.getenv("DATASET_WATCHLIST_1_PATHNAME"))
    df2 = pd.read_csv(os.getenv("DATASET_WATCHLIST_2_PATHNAME"))

    matching_movies = pd.merge(df1, df2, on="Name", how="inner", suffixes=("_1", "_2"))

    matching_movies["Year"] = (
        matching_movies[["Year_1", "Year_2"]].bfill(axis=1).iloc[:, 0]
    )
    matching_movies["Year"] = matching_movies["Year"].astype("Int64")

    matching_movies = matching_movies[["Name", "Year"]]

    matching_movies = generate_csv(matching_movies, "matching_movies.csv")

    return matching_movies
