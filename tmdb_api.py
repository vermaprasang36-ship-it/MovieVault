import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# ---------------------------------------------------
# Format Movie
# ---------------------------------------------------
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


# ---------------------------------------------------
# Fetch Movies
# ---------------------------------------------------
def fetch_movies(endpoint, params=None):

    if not API_KEY:
        print("TMDB API Key not found.")
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
        print("TMDB Error:", e)
        return []


# ---------------------------------------------------
# Search Movies
# ---------------------------------------------------
def search_movies(query):

    return fetch_movies(
        "/search/movie",
        {
            "query": query,
            "include_adult": False
        }
    )


# ---------------------------------------------------
# Popular Movies
# ---------------------------------------------------
def get_popular_movies():

    return fetch_movies("/movie/popular")


# ---------------------------------------------------
# Movie Details
# ---------------------------------------------------
def get_movie_details(movie_id):

    if not API_KEY:
        return None

    try:

        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            params={
                "api_key": API_KEY,
                "language": "en-US"
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return {

            "id": data.get("id"),

            "title": data.get("title"),

            "overview": data.get("overview"),

            "rating": data.get("vote_average"),

            "release_date": data.get("release_date"),

            "runtime": data.get("runtime"),

            "genres": [
                genre["name"]
                for genre in data.get("genres", [])
            ],

            "language": data.get("original_language"),

            "poster_url": (
                f"{IMAGE_BASE_URL}{data.get('poster_path')}"
                if data.get("poster_path")
                else None
            ),

            "backdrop_url": (
                f"{IMAGE_BASE_URL}{data.get('backdrop_path')}"
                if data.get("backdrop_path")
                else None
            ),
        }

    except requests.exceptions.RequestException as e:

        print("Movie Details Error:", e)

        return None


# ---------------------------------------------------
# Movie Trailer
# ---------------------------------------------------
def get_movie_trailer(movie_id):
    if not API_KEY:
        return None

    try:
        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}/videos",
            params={
                "api_key": API_KEY,
                "language": "en-US"
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        videos = data.get("results", [])

        # Try to find any YouTube video
        for video in videos:
            if video.get("site") == "YouTube":
                return f"https://www.youtube.com/watch?v={video['key']}"

        # Fallback to YouTube search if no trailer exists
        movie = get_movie_details(movie_id)

        if movie:
            title = movie["title"].replace(" ", "+")
            return (
                f"https://www.youtube.com/results"
                f"?search_query={title}+official+trailer"
            )

        return None

    except requests.exceptions.RequestException as e:
        print("Trailer Error:", e)
        return None

# ---------------------------------------------------
# Test
# ---------------------------------------------------
if __name__ == "__main__":

    movies = get_popular_movies()

    print("Movies:", len(movies))

    if movies:
        movie_id = movies[0]["id"]

        trailer = get_movie_trailer(movie_id)

        print("Trailer:", trailer)

#.\.venv\Scripts\python.exe tmdb_api.py
# Expected
# No traceback
# No syntax errors
# No import errors
# It may produce no output, and it's completely fine because this file only defins fnctions
