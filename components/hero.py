import streamlit as st

from database import (
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)


# ==========================================
# Hero Image
# ==========================================
def render_hero_image(movie):

    if movie.get("backdrop_url"):

        st.image(
            movie["backdrop_url"],
            use_container_width=True,
        )


# ==========================================
# Hero Information
# ==========================================
def render_hero_info(movie):

    with st.container(border=True):

        st.markdown("### 🔥 Trending Now")

        st.markdown(f"# 🎬 {movie['title']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"⭐ **{movie['rating']} / 10**")

        with col2:
            st.markdown(f"📅 **{movie['release_date']}**")

        st.markdown("")

        btn1, btn2, btn3 = st.columns(3)

        # -------------------------
        # Watchlist
        # -------------------------
        with btn1:

            if is_movie_in_watchlist(movie["id"]):

                st.button(
                    "❤️ In Watchlist",
                    disabled=True,
                    key=f"hero_saved_{movie['id']}",
                    use_container_width=True
                )

            else:

                if st.button(
                    "❤️ Add to Watchlist",
                    key=f"hero_add_{movie['id']}",
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

        # -------------------------
        # Trailer
        # -------------------------
        with btn2:

            if st.button(
                "▶ Watch Trailer",
                key=f"hero_trailer_{movie['id']}",
                use_container_width=True
            ):

                st.session_state["selected_movie"] = movie["id"]

                st.switch_page("pages/movie_details.py")

        # -------------------------
        # Details
        # -------------------------
        with btn3:

            if st.button(
                "ℹ View Details",
                key=f"hero_details_{movie['id']}",
                use_container_width=True
            ):

                st.session_state["selected_movie"] = movie["id"]

                st.switch_page("pages/movie_details.py")


# ==========================================
# Complete Hero
# ==========================================
def render_hero(movie):

    if not movie:
        return

    render_hero_image(movie)

    st.markdown("")

    render_hero_info(movie)

    st.markdown("<br>", unsafe_allow_html=True)