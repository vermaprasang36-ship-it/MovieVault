import streamlit as st

from database import (
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)


def render_movie_card(movie, unique_key):
    """Render a premium movie card."""

    with st.container(border=True):

        # ----------------------------
        # Poster
        # ----------------------------
        poster = movie.get("poster_url")

        if poster:
            st.image(
                poster,
                use_container_width=True,
            )

        # ----------------------------
        # Title
        # ----------------------------
        title = movie.get("title", "Unknown Movie")

        st.markdown(
            f"""
            <div style="
            font-size:22px;
            font-weight:700;
            line-height:1.3;
            height:60px;
            overflow:hidden;
            margin-top:12px;
            margin-bottom:12px;
            ">
            {title}
            </div>
            """,
            unsafe_allow_html=True,
            )

        # ----------------------------
        # Rating + Year
        # ----------------------------
        rating = movie.get("rating", "N/A")

        release_date = movie.get("release_date", "")
        year = release_date[:4] if release_date else "----"

        st.markdown(
            f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">

<span style="
background:#E50914;
color:white;
padding:5px 12px;
border-radius:999px;
font-size:14px;
font-weight:600;
">
⭐ {rating}
</span>

<span style="
color:#B7BDC9;
font-size:14px;
font-weight:500;
">
📅 {year}
</span>

</div>
""",
            unsafe_allow_html=True,
        )

        # ----------------------------
        # Overview
        # ----------------------------
        overview = movie.get("overview", "")

        if len(overview) > 130:
            overview = overview[:130].rstrip() + "..."

        st.markdown(
            f"""
<div style="
color:#C5CAD5;
font-size:14px;
line-height:1.6;
height:95px;
overflow:hidden;
margin-bottom:18px;
">
{overview}
</div>
""",
            unsafe_allow_html=True,
        )

        # ----------------------------
        # Buttons
        # ----------------------------
        col1, col2 = st.columns(2, gap="small")

        with col1:

            if is_movie_in_watchlist(movie["id"]):

                st.button(
                    "❤️ Saved",
                    disabled=True,
                    key=f"saved_{unique_key}",
                    use_container_width=True,
                )

            else:

                if st.button(
                    "❤️ Save",
                    key=f"watch_{unique_key}",
                    use_container_width=True,
                ):

                    add_movie_to_watchlist(
                        movie["id"],
                        movie["title"],
                        movie["release_date"],
                        movie["rating"],
                        movie["overview"],
                        movie["poster_url"],
                    )

                    st.toast("Added to Watchlist ❤️")

                    st.rerun()

        with col2:

            if st.button(
                "ℹ Details",
                key=f"details_{unique_key}",
                use_container_width=True,
            ):

                st.session_state["selected_movie"] = movie["id"]

                st.switch_page("pages/movie_details.py")

