import streamlit as st

from tmdb_api import (
    get_popular_movies,
    get_trending_movies,
)

from components.metrics import render_metrics
import components.hero as hero

from database import (
    create_tables,
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)




# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Create Database
# -----------------------------
create_tables()

# -----------------------------
# Load CSS
# -----------------------------
def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
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
# -----------------------------
# Search + Watchlist Button
# -----------------------------

col1, col2 = st.columns([5, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search for a movie..."
    )

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
# Popular Movies
# -----------------------------
st.subheader("🔥 Popular Movies")

cols = st.columns(3)

for index, movie in enumerate(movies):

    unique_key = f"{movie['id']}_{index}"

    with cols[index % 3]:

        with st.container(border=True):

            if movie["poster_url"]:
                st.image(
                    movie["poster_url"],
                    use_container_width=True
                )

            st.markdown(f"### 🎬 {movie['title']}")

            st.write(f"⭐ **Rating:** {movie['rating']}")
            st.write(f"📅 **Release:** {movie['release_date']}")

            # -----------------------------
            # Watchlist Button
            # -----------------------------
            if is_movie_in_watchlist(movie["id"]):

                st.button(
                    " ❤️ In Watchlist",
                    disabled=True,
                    key=f"saved_{unique_key}",
                    use_container_width=True
                )

            else:

                if st.button(
                    "❤️ Add to Watchlist",
                    key=f"watchlist_{unique_key}",
                    use_container_width=True
                ):

                    add_movie_to_watchlist(
                        movie["id"],
                        movie["title"],
                        movie["release_date"],
                        movie["rating"],
                        movie["overview"],
                        movie["poster_url"]
                    )

                    st.toast("❤️ Added to Watchlist!")

                    st.rerun()

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
   
