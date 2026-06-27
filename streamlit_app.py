import streamlit as st

from tmdb_api import get_popular_movies

st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 MovieVault")

st.subheader("🔥 Popular Movies")

movies = get_popular_movies()

for movie in movies:
    st.markdown("---")

    st.subheader(movie["title"])

    st.write(f"⭐ Rating: {movie['rating']}")

    st.write(f"📅 Release Date: {movie['release_date']}")