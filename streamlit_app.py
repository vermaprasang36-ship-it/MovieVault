import streamlit as st

from tmdb_api import (
    get_popular_movies,
    get_trending_movies,
    get_top_rated_movies,
    get_movies_by_genre,
    search_movies,
    GENRES,
)


from components.metrics import render_metrics

from components import hero_html as hero


from database import (
    create_tables,
    add_movie_to_watchlist,
    is_movie_in_watchlist,
)

from components.movie_card import render_movie_card




# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MovieVault",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Create Database
# -----------------------------
create_tables()

# -----------------------------
# Load CSS
# -----------------------------
def load_css():

    css_files = [
    "styles/theme.css",
    "styles/buttons.css",
    "styles/hero.css",
    "styles/cards.css",
    "styles/layout.css",
]

    css = ""

    for file in css_files:
        with open(file, encoding="utf-8") as f:
            css += f.read() + "\n"

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


load_css()

with open("styles/hero.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    ) 


# -----------------------------
# Session State
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "movies" not in st.session_state:
    st.session_state.movies = get_popular_movies(
        page=st.session_state.page
    )

# Remove duplicate movies
unique_movies = []
seen_ids = set()

for movie in st.session_state.movies:

    if movie["id"] not in seen_ids:
        unique_movies.append(movie)
        seen_ids.add(movie["id"])

# Final unique movie list
movies = unique_movies

# Fetch trending movies for the hero
trending_movies = get_trending_movies()
top_rated_movies = get_top_rated_movies()

# -----------------------------
# Hero Movies (Top 5 Trending)
# -----------------------------
hero_movies = trending_movies[:5]

# -----------------------------
# Hero Slider State
# -----------------------------
if "hero_index" not in st.session_state:
    st.session_state.hero_index = 0

# -----------------------------
# Genre Session
# -----------------------------
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = None

# -----------------------------
# Hero Movie
# -----------------------------
if hero_movies:

    featured_movie = hero_movies[
        st.session_state.hero_index
    ]

else:

    featured_movie = (
        movies[0]
        if movies
        else None
    )


# -----------------------------
# Header
# -----------------------------
st.title("🎬 MovieVault AI")

st.caption("Discover • Explore • Watch")

hero_container = st.container()

with hero_container:

    hero.render_hero(
        hero_movies,
        st.session_state.hero_index
    )

    left_arrow, dots, right_arrow = st.columns([1, 8, 1])


with left_arrow:

    if st.button(
        "⬅",
        key="hero_left",
        use_container_width=True
    ):

        if st.session_state.hero_index > 0:

            st.session_state.hero_index -= 1

            st.rerun()

with right_arrow:

    if st.button(
        "➡",
        key="hero_right",
        use_container_width=True
    ):

        if st.session_state.hero_index < len(hero_movies) - 1:

            st.session_state.hero_index += 1

            st.rerun()

with dots:

    dots = ""

for i in range(len(hero_movies)):

    if i == st.session_state.hero_index:
        dots += "🔴 "
    else:
        dots += "⚪ "

st.markdown(
    f"""
    <div style="text-align:center;font-size:20px;">
        {dots}
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("###")

b1, b2, b3 = st.columns(3)

with b1:

    if is_movie_in_watchlist(featured_movie["id"]):

        st.button(
            "❤️ In Watchlist",
            disabled=True,
            use_container_width=True
        )

    else:

        if st.button(
            "❤️ Add to Watchlist",
            use_container_width=True,
            key="hero_watchlist"
        ):

            add_movie_to_watchlist(
                featured_movie["id"],
                featured_movie["title"],
                featured_movie["release_date"],
                featured_movie["rating"],
                featured_movie["overview"],
                featured_movie["poster_url"]
            )

            st.rerun()

with b2:

    if st.button(
        "▶ Watch Trailer",
        use_container_width=True,
        key="hero_trailer"
    ):

        st.session_state["selected_movie"] = featured_movie["id"]

        st.switch_page("pages/movie_details.py")

with b3:

    if st.button(
        "ℹ View Details",
        use_container_width=True,
        key="hero_details"
    ):

        st.session_state["selected_movie"] = featured_movie["id"]

        st.switch_page("pages/movie_details.py")

st.markdown("---")
# -----------------------------
# Search + Watchlist Button
# -----------------------------

col1, col2 = st.columns([5, 1])

with col1:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search for a movie..."
    )

# -----------------------------
# Search Movies
# -----------------------------
if search_query.strip():

    movies = search_movies(search_query)

else:

    movies = unique_movies

with col2:
    st.write("")
    st.write("")

    if st.button(
        "❤️ My Watchlist",
        use_container_width=True
    ):
        st.switch_page("pages/watchlist.py")

# -----------------------------
# Dashboard Metrics
# -----------------------------
render_metrics(movies)

st.markdown("---")

# -----------------------------
# Trending Slider State
# -----------------------------
if "trending_index" not in st.session_state:
    st.session_state.trending_index = 0

# -----------------------------
# Trending Today
# -----------------------------
st.subheader("🔥 Trending Today")

left, center, right = st.columns([1, 8, 1])

# Left Arrow
with left:

    if st.button("⬅", key="trending_left"):

        if st.session_state.trending_index > 0:
            st.session_state.trending_index -= 1

# Right Arrow
with right:

    if st.button("➡", key="trending_right"):

        if st.session_state.trending_index < len(trending_movies) - 4:
            st.session_state.trending_index += 1

# Visible Movies
visible_movies = trending_movies[
    st.session_state.trending_index:
    st.session_state.trending_index + 4
]

with center:

    cols = st.columns(4)

    for col, movie in zip(cols, visible_movies):

        with col:

            render_movie_card(
                movie,
                f"trending_{movie['id']}"
            )

st.markdown("---")

# -----------------------------
# Genre Slider State
# -----------------------------
if "genre_index" not in st.session_state:
    st.session_state.genre_index = 0

# -----------------------------
# Browse by Genre
# -----------------------------
st.subheader("🎭 Browse by Genre")

genre_names = list(GENRES.keys())

left, center, right = st.columns([1, 8, 1])

# -----------------------------
# Left Arrow
# -----------------------------
with left:

    if st.button("⬅", key="genre_left"):

        if st.session_state.genre_index > 0:
            st.session_state.genre_index -= 1

# -----------------------------
# Right Arrow
# -----------------------------
with right:

    if st.button("➡", key="genre_right"):

        if st.session_state.genre_index < len(genre_names) - 4:
            st.session_state.genre_index += 1

# -----------------------------
# Visible Genres
# -----------------------------
visible_genres = genre_names[
    st.session_state.genre_index :
    st.session_state.genre_index + 4
]

with center:

    cols = st.columns(4)

    for col, genre in zip(cols, visible_genres):

        with col:

            if st.button(
                genre,
                key=f"genre_{genre}",
                use_container_width=True,
            ):

                st.session_state.selected_genre = genre

# -----------------------------
# Selected Genre Movies
# -----------------------------
if st.session_state.selected_genre:

    st.markdown("---")

    st.subheader(
        f"🎬 {st.session_state.selected_genre} Movies"
    )

    genre_movies = get_movies_by_genre(
        GENRES[st.session_state.selected_genre]
    )

    genre_movie_cols = st.columns(4)

    for index, movie in enumerate(genre_movies[:8]):

        with genre_movie_cols[index % 4]:

            render_movie_card(
                movie,
                f"genre_{movie['id']}"
            )

    st.markdown("---")

    # -----------------------------
# Top Rated Slider State
# -----------------------------
if "top_rated_index" not in st.session_state:
    st.session_state.top_rated_index = 0



# -----------------------------
# Top Rated Movies
# -----------------------------
st.subheader("⭐ Top Rated Movies")

top_cols = st.columns(4)

for index, movie in enumerate(top_rated_movies[:4]):

    with top_cols[index]:

        render_movie_card(
            movie,
            f"top_{movie['id']}"
        )

st.markdown("---")



# -----------------------------
# Popular Movies
# -----------------------------
st.subheader("🔥 Popular Movies")

cols = st.columns(3)

for index, movie in enumerate(movies):

    unique_key = f"{movie['id']}_{index}"

    with cols[index % 3]:

        render_movie_card(
            movie,
            unique_key
        )



# -----------------------------
# Load More Movies
# -----------------------------
st.markdown("###")

if st.button(
    "⬇ Load 20 More Movies",
    use_container_width=True
):

    st.session_state.page += 1

    new_movies = get_popular_movies(
        page=st.session_state.page
    )

    # Existing movie IDs
    existing_ids = {
        movie["id"]
        for movie in st.session_state.movies
    }

    # Add only new movies
    for movie in new_movies:

        if movie["id"] not in existing_ids:
            st.session_state.movies.append(movie)

    st.rerun()

    #.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py   ----  to run on terminal
   
 