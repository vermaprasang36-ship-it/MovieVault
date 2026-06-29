import streamlit as st


def render_hero():
    st.title("🎬 MovieVault AI")
    st.subheader("Discover your next favorite movie")
    st.write("Hero component is working.")

    search_query = st.text_input(
        "",
        placeholder="🔍 Search for a movie..."
    )

    return search_query