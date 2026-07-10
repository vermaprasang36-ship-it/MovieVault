import streamlit as st

from tmdb_api import (
    get_movie_details,
    get_movie_trailer,
    get_similar_movies,
)

from database import (
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Movie Details",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Hero Section
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🎬 Movie Details</h1>
        <h3>Everything you need to know</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Get Selected Movie
# -----------------------------
movie_id = st.session_state.get("selected_movie")

if movie_id:

    movie = get_movie_details(movie_id)
    trailer_url = get_movie_trailer(movie_id)
    similar_movies = get_similar_movies(movie_id)
    if movie:

        # -----------------------------
        # Backdrop Image
        # -----------------------------
        if movie.get("backdrop_url"):
            st.image(
                movie["backdrop_url"],
                use_container_width=True
            )

        st.markdown("---")

        # -----------------------------
        # Movie Layout
        # -----------------------------
        left, right = st.columns([1, 2])

        with left:
            if movie.get("poster_url"):
                st.image(
                    movie["poster_url"],
                    use_container_width=True
                )

        with right:

            st.title(movie["title"])

            st.markdown(
                f"""
                <span class="rating-badge">
                    ⭐ {movie['rating']} / 10
                </span>
                """,
                unsafe_allow_html=True
            )

            st.write(f"📅 **Release:** {movie['release_date']}")
            st.write(f"⏱ **Runtime:** {movie['runtime']} min")
            st.write(f"🌍 **Language:** {movie['language']}")

            # -----------------------------
            # Genres
            # -----------------------------
            st.markdown("### 🎭 Genres")

            genre_cols = st.columns(len(movie["genres"]))

            for col, genre in zip(genre_cols, movie["genres"]):

                with col:
                    st.info(genre)

            st.markdown("---")

            # -----------------------------
            # Overview
            # -----------------------------
            st.markdown("## 📖 Overview")

            st.write(movie["overview"])

            st.markdown("###")

            # -----------------------------
            # Action Buttons
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:

                if is_movie_in_watchlist(movie["id"]):

                    st.button(
                        "❤️ In Watchlist",
                        disabled=True,
                        use_container_width=True
                    )

                else:

                    if st.button(
                        "❤️ Add to Watchlist",
                        key="details_watchlist",
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

                        st.success("✅ Added to Watchlist!")

                        st.rerun()

            with col2:

                if trailer_url:

                    st.video(trailer_url)
                
                else:

                    st.button(
                        "❌ Trailer Not Available",
                        disabled=True,
                        use_container_width=True
                    )


    else:
        st.error("❌ Movie not found.")

else:
    st.info("👈 Please select a movie from the Home page.")


st.markdown("---")
st.subheader("🎬 You May Also Like")

if similar_movies:

    cols = st.columns(4)

    for index, similar in enumerate(similar_movies[:4]):

        with cols[index]:

            with st.container(border=True):

                if similar.get("poster_url"):

                    st.image(
                        similar["poster_url"],
                        use_container_width=True
                    )

                st.markdown(f"**{similar['title']}**")

                st.caption(f"⭐ {similar['rating']}")

                if st.button(
                    "🎬 View Details",
                    key=f"similar_{similar['id']}",
                    use_container_width=True
                ):

                    st.session_state["selected_movie"] = similar["id"]

                    st.rerun()
# -----------------------------
# Back Button
# -----------------------------
st.markdown("---")

if st.button(
    "⬅ Back to Home",
    use_container_width=True
):
    st.switch_page("streamlit_app.py")