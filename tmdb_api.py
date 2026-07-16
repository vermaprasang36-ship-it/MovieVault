import os
import requests
from dotenv import load_dotenv

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
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
        "rating": round(movie.get("vote_average", 0), 1),
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
# Generic Movie Fetcher
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
# Popular Movies
# ---------------------------------------------------
def get_popular_movies(page=1):

    return fetch_movies(
        "/movie/popular",
        {
            "page": page
        }
    )

# ---------------------------------------------------
# Top Rated Movies
# ---------------------------------------------------
def get_top_rated_movies(page=1):

    return fetch_movies(
        "/movie/top_rated",
        {
            "page": page
        }
    )

# ---------------------------------------------------
# Genre Movies
# ---------------------------------------------------
def get_movies_by_genre(genre_id, page=1):

    return fetch_movies(
        "/discover/movie",
        {
            "with_genres": genre_id,
            "page": page
        }
    )

GENRES = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Sci-Fi": 878,
    "Thriller": 53,
}

# ---------------------------------------------------
# Trending Movies
# ---------------------------------------------------
def get_trending_movies():

    return fetch_movies("/trending/movie/day")


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

            "rating": round(data.get("vote_average", 0), 1),

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
# Similar Movies
# ---------------------------------------------------
def get_similar_movies(movie_id):

    return fetch_movies(
        f"/movie/{movie_id}/similar"
    )    


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
            timeout=20
        )

        response.raise_for_status()

        videos = response.json().get("results", [])

        # Prefer official trailer
        for video in videos:

            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
            ):

                return (
                    f"https://www.youtube.com/watch?v={video['key']}"
                )

        # Fallback to any YouTube video
        for video in videos:

            if video.get("site") == "YouTube":

                return (
                    f"https://www.youtube.com/watch?v={video['key']}"
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

        print("\nFirst Movie:\n")

        print(movies[0])

        print("\nTrailer:\n")

        print(get_movie_trailer(movies[0]["id"]))

        
#.\.venv\Scripts\python.exe tmdb_api.py
# Expected
# No traceback
# No syntax errors
# No import errors
# It may produce no output, and it's completely fine because this file only defins fnctions
