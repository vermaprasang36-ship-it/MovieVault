import streamlit as st
from tmdb_api import (
    get_movie_details,
    get_movie_trailer
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

            genres = " • ".join(movie["genres"])
            st.write(f"🎭 **Genres:** {genres}")

            st.markdown("### Overview")
            st.write(movie["overview"])

            st.markdown("###")

            # -----------------------------
            # Action Buttons
            # -----------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.button(
                    "❤️ Add to Watchlist",
                    key="details_watchlist",
                    use_container_width=True
                )

            with col2:
                if trailer_url:
                    st.link_button(
                        "▶ Watch Trailer",
                        trailer_url,
                        use_container_width=True
                    )
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

# -----------------------------
# Back Button
# -----------------------------
st.markdown("---")

if st.button(
    "⬅ Back to Home",
    use_container_width=True
):
    st.switch_page("streamlit_app.py")