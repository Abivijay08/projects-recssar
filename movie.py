import streamlit as st
import requests
import os
from groq import Groq
from dotenv import load_dotenv

# -----------------------------------
# LOAD ENV
# -----------------------------------

load_dotenv()
GROQ_API_KEY = os.getenv("ABI")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Movie Review Generator",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.title {
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:#ff4b4b;
}

.movie-box{
    background:#f8f9fa;
    padding:20px;
    border-radius:15px;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------

st.markdown(
    "<p class='title'>🎬 AI Movie Review Platform</p>",
    unsafe_allow_html=True
)

st.write(
    "Search any movie and get details, ratings, cast, genre and AI review."
)

st.divider()

# -----------------------------------
# MOVIE INPUT
# -----------------------------------

movie_name = st.text_input(
    "Enter Movie Name",
    placeholder="Example: Interstellar"
)

# -----------------------------------
# SEARCH BUTTON
# -----------------------------------

if st.button("Search Movie"):

    if not movie_name:
        st.warning("Please enter a movie name.")
        st.stop()

    # -----------------------------------
    # OMDB API
    # -----------------------------------

    url = (
        f"http://www.omdbapi.com/?t={movie_name}"
        f"&apikey={OMDB_API_KEY}"
    )

    response = requests.get(url)

    movie = response.json()

    if movie["Response"] == "False":
        st.error("Movie not found.")
        st.stop()

    # -----------------------------------
    # MOVIE DETAILS
    # -----------------------------------

    title = movie.get("Title", "N/A")
    year = movie.get("Year", "N/A")
    genre = movie.get("Genre", "N/A")
    director = movie.get("Director", "N/A")
    actors = movie.get("Actors", "N/A")
    plot = movie.get("Plot", "N/A")
    rating = movie.get("imdbRating", "N/A")
    poster = movie.get("Poster", "")

    # -----------------------------------
    # POSTER
    # -----------------------------------

    if poster != "N/A":
        st.image(
            poster,
            width=300
        )

    # -----------------------------------
    # DETAILS
    # -----------------------------------

    st.subheader("🎥 Movie Details")

    st.markdown(f"""
    **Title:** {title}

    **Year:** {year}

    **Genre:** {genre}

    **Director:** {director}

    **Actors / Actress:** {actors}

    **IMDb Rating:** ⭐ {rating}
    """)

    st.divider()

    # -----------------------------------
    # AI REVIEW
    # -----------------------------------

    with st.spinner("Generating AI Review..."):

        prompt = f"""
        You are a professional movie critic.

        Movie Name: {title}

        Plot:
        {plot}

        Genre:
        {genre}

        IMDb Rating:
        {rating}

        Give:

        1. Professional Review
        2. Strengths
        3. Weaknesses
        4. Final Verdict
        5. Recommendation Score out of 10

        Use headings.
        """

        review_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        review = (
            review_response
            .choices[0]
            .message
            .content
        )

    st.subheader("🤖 AI Movie Review")

    st.markdown(review)

    st.divider()

    # -----------------------------------
    # DOWNLOAD REVIEW
    # -----------------------------------

    download_text = f"""
Movie: {title}

Genre: {genre}

Director: {director}

Actors: {actors}

IMDb Rating: {rating}

AI Review:

{review}
"""

    st.download_button(
        label="📄 Download Review",
        data=download_text,
        file_name=f"{title}_review.txt",
        mime="text/plain"
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "Powered by OMDb API + Groq AI"
)