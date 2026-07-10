import streamlit as st

from database import (
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)


def render_movie_card(movie, unique_key):

    with st.container(border=True):

        if movie["poster_url"]:
            st.image(
                movie["poster_url"],
                use_container_width=True
            )

        st.markdown(f"### 🎬 {movie['title']}")

        st.markdown(
            f"⭐ **{movie['rating']}** &nbsp;&nbsp;&nbsp; "
            f"📅 **{movie['release_date']}**",
            unsafe_allow_html=True
        )

        overview = movie.get("overview", "")

        if len(overview) > 120:
            overview = overview[:120] + "..."

        st.caption(overview)

        col1, col2 = st.columns(2)

        with col1:

            if is_movie_in_watchlist(movie["id"]):

                st.button(
                    "❤️ Saved",
                    disabled=True,
                    key=f"saved_{unique_key}",
                    use_container_width=True
                )

            else:

                if st.button(
                    "❤️ Save",
                    key=f"watch_{unique_key}",
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

                    st.toast("Added to Watchlist ❤️")

                    st.rerun()

        with col2:

            if st.button(
                "ℹ Details",
                key=f"details_{unique_key}",
                use_container_width=True
            ):

                st.session_state["selected_movie"] = movie["id"]

                st.switch_page("pages/movie_details.py")