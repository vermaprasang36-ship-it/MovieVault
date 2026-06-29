import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def format_movie(movie):
    poster_path = movie.get("poster_path")
    backdrop_path = movie.get("backdrop_path")

    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "rating": movie.get("vote_average"),
        "overview": movie.get("overview"),

        "poster_url": (
            f"{IMAGE_BASE_URL}{poster_path}"
            if poster_path else None
        ),

        "backdrop_url": (
            f"{IMAGE_BASE_URL}{backdrop_path}"
            if backdrop_path else None
        ),
    }
    

def fetch_movies(endpoint, params=None):
    if not API_KEY:
        print("TMDB API key is missing. Please check your .env file.")
        return []

    request_params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    if params:
        request_params.update(params)

    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            params=request_params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()
        movies = data.get("results", [])

        formatted = [format_movie(movie) for movie in movies]

        print("=" * 50)
        print("RETURNING FROM fetch_movies()")
        print(formatted[0])
        print("=" * 50)

        return formatted
        
        print("Returning from fetch_movies():")
        print(formatted[0])

    except requests.exceptions.RequestException as e:
        print(f"TMDB Error: {e}")
        return []

def search_movies(query):
    return fetch_movies(
        "/search/movie",
        {
            "query": query,
            "include_adult": False,
        },
    )

def get_popular_movies():
    return fetch_movies("/movie/popular")


if __name__ == "__main__":
    movies = get_popular_movies()

    print("Movies:", len(movies))


#.\.venv\Scripts\python.exe tmdb_api.py
# Expected
# No traceback
# No syntax errors
# No import errors
# It may produce no output, and it's completely fine because this file only defins fnctions
