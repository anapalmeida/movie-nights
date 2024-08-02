from dotenv import load_dotenv

import os
import requests

load_dotenv()


def get_cast_n_crew(movie_id):
    api_url = os.getenv("TMDB_API_URL")
    api_token = os.getenv("TMDB_API_TOKEN")

    if not api_url or not api_token:
        print("API URL or Token not found in .env file")
        return None

    api_url += f"/movie/{movie_id}/credits?language=en-US"

    headers = {"accept": "application/json", "Authorization": f"Bearer {api_token}"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        cast = response.json().get("cast")
        crew = response.json().get("crew")

        results = {
            "cast": cast,
            "director":  [person for person in crew if person.get("job") == "Director"],
            "writer":  [person for person in crew if person.get("job") == "Writer"]
        }

        return results

    print("Error:", response.status_code, response.text)
    return None