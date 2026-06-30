import streamlit as st

from tmdb_api import get_popular_movies
from components.metrics import render_metrics
from database import (
    create_tables,
    add_movie_to_watchlist
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
movies = get_popular_movies()

featured_movie = movies[0] if movies else None

# -----------------------------
# Hero Section
# -----------------------------
st.markdown("""
<div class="hero">

<h1>🎬 MovieVault AI</h1>

<h3>Discover your next favorite movie</h3>

<p>
Browse millions of movies, build your watchlist,
and soon get <b>AI-powered recommendations.</b>
</p>

</div>
""", unsafe_allow_html=True)

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
# Featured Movie
# -----------------------------
st.markdown("## 🌟 Featured Movie")

if featured_movie:

    left, right = st.columns([1.2, 2.8])

    with left:

        image_url = (
            featured_movie.get("backdrop_url")
            or featured_movie.get("poster_url")
        )

        if image_url:
            st.image(
                image_url,
                use_container_width=True
            )

    with right:

        st.markdown(f"# {featured_movie['title']}")

        st.markdown(
            f"""
            <span class="rating-badge">
                ⭐ {featured_movie['rating']} / 10
            </span>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"📅 **Released:** {featured_movie['release_date']}"
        )

        overview = featured_movie["overview"]

        if len(overview) > 180:
            overview = overview[:180] + "..."

        st.write(overview)

        col1, col2 = st.columns(2)

        # -----------------------------
        # Featured Movie Buttons
        # -----------------------------
        with col1:

            if st.button(
                "❤️ Add to Watchlist",
                key="featured_watchlist"
            ):

                add_movie_to_watchlist(
                    featured_movie["id"],
                    featured_movie["title"],
                    featured_movie["release_date"],
                    featured_movie["rating"],
                    featured_movie["overview"],
                    featured_movie["poster_url"]
                )

                st.success(
                    f"✅ {featured_movie['title']} added to Watchlist!"
                )

        with col2:

            if st.button(
                "🎥 View Details",
                key="featured_details"
            ):

                st.session_state["selected_movie"] = featured_movie["id"]
                st.switch_page("pages/movie_details.py")

st.markdown("---")

# -----------------------------
# Popular Movies
# -----------------------------
st.subheader("🔥 Popular Movies")

cols = st.columns(3)

for index, movie in enumerate(movies):

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

            if st.button(
                "❤️ Add to Watchlist",
                key=f"watchlist_{movie['id']}"
            ):

                add_movie_to_watchlist(
                    movie["id"],
                    movie["title"],
                    movie["release_date"],
                    movie["rating"],
                    movie["overview"],
                    movie["poster_url"]
                )

                st.success(
                    f"✅ {movie['title']} added to Watchlist!"
                )


    #.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py   ----  to run on terminal
   