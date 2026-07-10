import streamlit as st

from tmdb_api import (
    get_popular_movies,
    get_trending_movies,
    get_top_rated_movies,
    search_movies,
)

from components.metrics import render_metrics
import components.hero as hero


from database import (
    create_tables,
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)

from components.movie_card import render_movie_card




# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Create Database
# -----------------------------
create_tables()

# -----------------------------
# Load CSS
# -----------------------------
def load_css():

    css_files = [
        "styles/theme.css",
        "styles/buttons.css",
        "styles/hero.css",
        "styles/cards.css",
    ]

    css = ""

    for file in css_files:
        with open(file, encoding="utf-8") as f:
            css += f.read() + "\n"

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


load_css()

# -----------------------------
# Fetch Movies
# -----------------------------
# -----------------------------
# Session State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "movies" not in st.session_state:
    st.session_state.movies = get_popular_movies(
        page=st.session_state.page
    )

# Remove duplicate movies
unique_movies = []
seen_ids = set()

for movie in st.session_state.movies:

    if movie["id"] not in seen_ids:
        unique_movies.append(movie)
        seen_ids.add(movie["id"])

# Final unique movie list
movies = unique_movies

# Fetch trending movies for the hero
trending_movies = get_trending_movies()
top_rated_movies = get_top_rated_movies()

# Hero movie
if trending_movies:
    featured_movie = trending_movies[0]
else:
    featured_movie = movies[0] if movies else None


# -----------------------------
# Header
# -----------------------------
st.title("🎬 MovieVault AI")

st.caption("Discover • Explore • Watch")

hero.render_hero(featured_movie)

st.markdown("###")

b1, b2, b3 = st.columns(3)

with b1:

    if is_movie_in_watchlist(featured_movie["id"]):

        st.button(
            "❤️ In Watchlist",
            disabled=True,
            use_container_width=True
        )

    else:

        if st.button(
            "❤️ Add to Watchlist",
            use_container_width=True,
            key="hero_watchlist"
        ):

            add_movie_to_watchlist(
                featured_movie["id"],
                featured_movie["title"],
                featured_movie["release_date"],
                featured_movie["rating"],
                featured_movie["overview"],
                featured_movie["poster_url"]
            )

            st.rerun()

with b2:

    st.button(
        "▶ Watch Trailer",
        use_container_width=True,
        key="hero_trailer"
    )

with b3:

    st.button(
        "ℹ View Details",
        use_container_width=True,
        key="hero_details"
    )

st.markdown("---")
# -----------------------------
# Search + Watchlist Button
# -----------------------------

col1, col2 = st.columns([5, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search for a movie..."
    )

# -----------------------------
# Search Movies
# -----------------------------
if search_query.strip():

    movies = search_movies(search_query)

else:

    movies = unique_movies

with col2:
    st.write("")
    st.write("")

    if st.button(
        "❤️ My Watchlist",
        use_container_width=True
    ):
        st.switch_page("pages/watchlist.py")

# -----------------------------
# Dashboard Metrics
# -----------------------------
render_metrics(movies)

st.markdown("---")

# -----------------------------
# Top Rated Movies
# -----------------------------
st.subheader("⭐ Top Rated Movies")

top_cols = st.columns(4)

for index, movie in enumerate(top_rated_movies[:4]):

    with top_cols[index]:

        render_movie_card(
            movie,
            f"top_{movie['id']}"
        )

st.markdown("---")



# -----------------------------
# Popular Movies
# -----------------------------
st.subheader("🔥 Popular Movies")

cols = st.columns(3)

for index, movie in enumerate(movies):

    unique_key = f"{movie['id']}_{index}"

    with cols[index % 3]:

        render_movie_card(
            movie,
            unique_key
        )



# -----------------------------
# Load More Movies
# -----------------------------
st.markdown("###")

if st.button(
    "⬇ Load 20 More Movies",
    use_container_width=True
):

    st.session_state.page += 1

    new_movies = get_popular_movies(
        page=st.session_state.page
    )

    # Existing movie IDs
    existing_ids = {
        movie["id"]
        for movie in st.session_state.movies
    }

    # Add only new movies
    for movie in new_movies:

        if movie["id"] not in existing_ids:
            st.session_state.movies.append(movie)

    st.rerun()

    #.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py   ----  to run on terminal
   
