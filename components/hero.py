import streamlit as st


def render_hero(movie):

    if not movie:
        return

    with st.container():

        if movie.get("backdrop_url"):
            st.image(
                movie["backdrop_url"],
                use_container_width=True
            )

        st.markdown(f"# {movie['title']}")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"⭐ **{movie['rating']}**")

        with c2:
            st.markdown(f"📅 **{movie['release_date']}**")

        st.write(movie["overview"])