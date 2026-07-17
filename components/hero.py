import streamlit as st


def render_hero(movie):

    if not movie:
        return

    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)

    if movie.get("backdrop_url"):

        st.markdown('<div class="hero-image">', unsafe_allow_html=True)

        st.image(
            movie["backdrop_url"],
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero-info">

            <div class="hero-title">
                🎬 {movie["title"]}
            </div>

            <div class="hero-meta">
                ⭐ {movie["rating"]}
                &nbsp;&nbsp;&nbsp;
                📅 {movie["release_date"]}
            </div>

            <div class="hero-overview">
                {movie["overview"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)