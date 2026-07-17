import json
import streamlit.components.v1 as components


def render_hero(movies, current_index=0):

    if not movies:
        return

    movies_json = json.dumps(movies)

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<style>

* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

body {{
    background:transparent;
    font-family:Arial, Helvetica, sans-serif;
}}

.hero{{

    position:relative;

    width:100%;

    height:650px;

    border-radius:24px;

    overflow:hidden;

    box-shadow:
        0 25px 70px rgba(0,0,0,.55);

}}

.hero img{{

    width:100%;

    height:100%;

    object-fit:cover;

    transform:scale(1.03);

    animation:heroZoom 18s linear infinite alternate;

}}


.nav{{

    position:absolute;

    top:50%;

    transform:translateY(-50%);

    width:64px;

    height:64px;

    border:none;

    border-radius:50%;

    background:rgba(20,20,20,.45);

    backdrop-filter:blur(10px);

    color:white;

    font-size:34px;

    cursor:pointer;

    transition:all .25s ease;

    z-index:50;
}}

.nav:hover{{

    background:rgba(229,9,20,.90);

    transform:translateY(-50%) scale(1.08);

    box-shadow:
        0 0 30px rgba(229,9,20,.35);

}}



.left{{

left:25px;

}}

.right{{

right:25px;

}}


.content {{
    position:absolute;
    left:60px;
    bottom:55px;
    width:55%;
    color:white;
}}

.title{{

font-size:72px;

font-weight:800;

line-height:1.05;

letter-spacing:-1px;

margin-bottom:18px;

text-shadow:

0 4px 15px rgba(0,0,0,.45);

}}

.meta{{

display:flex;

gap:20px;

font-size:19px;

color:#E2E2E2;

margin-bottom:22px;

}}

.rating-badge{{

    display:inline-flex;

    align-items:center;

    justify-content:center;

    padding:8px 16px;

    background:#E50914;

    color:white;

    border-radius:999px;

    font-size:16px;

    font-weight:700;

    box-shadow:
        0 8px 18px rgba(229,9,20,.35);

}}

.overview{{

    max-width:760px;

    font-size:19px;

    line-height:1.75;

    color:#F3F3F3;

    text-shadow:
        0 2px 8px rgba(0,0,0,.4);

}}

.overlay{{

position:absolute;

inset:0;

background:

linear-gradient(
180deg,
rgba(0,0,0,.10) 0%,
rgba(0,0,0,.35) 45%,
rgba(0,0,0,.95) 100%
),

linear-gradient(
90deg,
rgba(0,0,0,.75) 0%,
rgba(0,0,0,.25) 45%,
rgba(0,0,0,0) 100%
);

}}



@keyframes heroZoom{{

from{{

transform:scale(1.03);

}}

to{{

transform:scale(1.10);

}}

}}

</style>

</head>

<body>

<div class="hero">

    <img id="heroImage">

    <div class="overlay"></div>

    <button id="prevBtn" class="nav left">
❮
</button>

<button id="nextBtn" class="nav right">
❯
</button>

    <div class="content">

        <div
            class="title"
            id="heroTitle">
        </div>

        <div class="meta">

            <div class="rating-badge" id="heroRating"></div>

            <div id="heroRelease"></div>

        </div>

        <div
            class="overview"
            id="heroOverview">
        </div>

    </div>

</div>

<script>

const movies = {movies_json};

let current = {current_index};


function renderMovie(index){{

    const movie = movies[index];

    document.getElementById("heroImage").src =
    movie.backdrop_url || "";

    document.getElementById("heroTitle").innerHTML =
        movie.title;

    document.getElementById("heroRating").innerHTML =
        "⭐ " + movie.rating + "/10";

    const year = (movie.release_date || "").slice(0,4);

    document.getElementById("heroRelease").innerHTML =
        "📅 " + year;

    document.getElementById("heroOverview").innerHTML =
        movie.overview;

}}

renderMovie(current);

console.log("Loaded Hero Movies");

console.log(movies);

document.getElementById("prevBtn").onclick = function () {{

    current--;

    if (current < 0) {{
        current = movies.length - 1;
    }}

    renderMovie(current);
}};

document.getElementById("nextBtn").onclick = function () {{

    current++;

    if (current >= movies.length) {{
        current = 0;
    }}

    renderMovie(current);
}};

let overview = movie.overview || "";

if (overview.length > 170){{
    overview = overview.substring(0,170) + "...";
}}

document.getElementById("heroOverview").innerHTML = overview;

</script>

</body>

</html>
"""

    components.html(
        html,
        height=620,
        scrolling=False,
    )