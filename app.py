import streamlit as st
import requests

# Set your TMDB API key here
tmdb_api_key = "924e31054eb99472ab9d97152c86b4a9"

# Genre mapping from TMDB
genre_mapping = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}

# Fetch poster
def fetch_poster(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={movie_title}"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        data = response.json()
        poster_path = data['results'][0]['poster_path'] if data['results'] else None
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        return None
    return None

# Fetch movies by genre
def get_movies_by_genre(genre_id):
    discover_url = f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&with_genres={genre_id}&language=en-US&sort_by=popularity.desc"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(discover_url, headers=headers, timeout=10)
        return response.json().get("results", [])
    except:
        return []

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎥 Movie Recommendation System")

# Sidebar filters
st.sidebar.header("🔎 Filters")

gender = st.sidebar.radio("Select your gender:", ["Male", "Female", "Other"])
preference = st.sidebar.selectbox("Select movie mood preference:", ["Any", "Emotional", "Thrilling", "Romantic", "Adventurous", "Comedic"])

selected_genre = st.sidebar.selectbox("Choose a genre:", list(genre_mapping.keys()))
genre_id = genre_mapping[selected_genre]

search_query = st.sidebar.text_input("Search movie by keyword (optional):")

st.markdown("### 🎞️ Recommended Movies:")

# Movie fetch logic
movies = get_movies_by_genre(genre_id)

if not movies:
    st.warning("No movies found or connection issue. Please try again.")
else:
    cols = st.columns(4)
    count = 0
    for movie in movies:
        title = movie.get("title", "No Title")
        vote = movie.get("vote_average", 0)
        overview = movie.get("overview", "No description available.")

        if search_query.lower() in title.lower() or search_query == "":
            with cols[count % 4]:
                poster_url = fetch_poster(title)
                if poster_url:
                    st.image(poster_url, width=180)
                st.markdown(f"**{title}**")
                stars = "⭐" * int(vote // 2) + "✩" * (5 - int(vote // 2))
                st.write(f"{stars} ({vote}/10)")
                with st.expander("📖 Overview"):
                    st.write(overview)
            count += 1

