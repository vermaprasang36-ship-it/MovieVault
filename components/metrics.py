import streamlit as st


def render_metrics(movies, watchlist_count=0):
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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎬 Movies", len(movies))

    with col2:
        st.metric("⭐ Avg Rating", avg_rating)

    with col3:
        st.metric("❤️ Watchlist", watchlist_count)