import streamlit as st
from database import get_all_watchlist_movies


def render_metrics(movies):
    """
    Render dashboard metrics.
    """

    if movies:
        avg_rating = round(
            sum(movie["rating"] for movie in movies) / len(movies),
            1
        )
    else:
        avg_rating = 0

    # Get watchlist count from database
    watchlist_count = len(get_all_watchlist_movies())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎬 Movies",
            len(movies)
        )

    with col2:
        st.metric(
            "⭐ Avg Rating",
            avg_rating
        )

    with col3:
        st.metric(
            "❤️ Watchlist",
            watchlist_count
        )