import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def format_movie(movie):
    poster_path = movie.get("poster_path")

    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "rating": movie.get("vote_average"),
        "overview": movie.get("overview"),
        "poster_url": f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None,
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

        return [format_movie(movie) for movie in movies]

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



