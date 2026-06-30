import streamlit as st

from database import (
    get_all_watchlist_movies,
    remove_movie_from_watchlist,
    update_watched_status
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="My Watchlist",
    page_icon="❤️",
    layout="wide"
)

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>❤️ My Watchlist</h1>
    <h3>Your saved movies</h3>
</div>
""", unsafe_allow_html=True)

movies = get_all_watchlist_movies()

if not movies:

    st.info("Your watchlist is empty.")

else:

    for movie in movies:

        with st.container(border=True):

            col1, col2 = st.columns([1, 3])

            with col1:

                if movie["poster_url"]:
                    st.image(
                        movie["poster_url"],
                        use_container_width=True
                    )

            with col2:

                st.markdown(f"## {movie['title']}")

                st.write(f"⭐ {movie['rating']}")

                st.write(f"📅 {movie['release_date']}")

                st.write(movie["overview"])

                watched = st.checkbox(
                    "Watched",
                    value=bool(movie["watched"]),
                    key=f"watched_{movie['tmdb_id']}"
                )

                update_watched_status(
                    movie["tmdb_id"],
                    watched
                )

                if st.button(
                    "🗑 Remove",
                    key=f"remove_{movie['tmdb_id']}"
                ):

                    remove_movie_from_watchlist(
                        movie["tmdb_id"]
                    )

                    st.rerun()

st.markdown("---")

if st.button(
    "⬅ Back to Home",
    use_container_width=True
):
    st.switch_page("streamlit_app.py")