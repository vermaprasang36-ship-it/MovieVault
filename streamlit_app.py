import streamlit as st

from tmdb_api import get_popular_movies
from components.metrics import render_metrics

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide"
)

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

search_query = st.text_input(
    "",
    placeholder="🔍 Search for a movie..."
)

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

        with col1:
            st.button(
                "❤️ Add to Watchlist",
                key="featured_watchlist"
            )

        with col2:
            st.button(
                "🎥 View Details",
                key="featured_details"
            )

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

            st.button(
                "❤️ Add to Watchlist",
                key=f"watchlist_{movie['id']}"
            )


    #.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py   ----  to run on terminal
   