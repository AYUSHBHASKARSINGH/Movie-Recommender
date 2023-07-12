import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image

# API key for themoviedb.org
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return None

# Function to recommend movies
def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = [] 
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

# Streamlit app settings
st.set_page_config(
    page_title="Movie Recommender",
    page_icon=":movie_camera:",
    layout="wide"
)

# App title and header
st.title("Movie Recommender System")
st.header("Discover Movies Similar to Your Favorites")

# Movie selection dropdown
selected_movie_name = st.selectbox('Select a Movie', movies['title'].values)

# Recommendation button
if st.button('Get Recommendations'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name, movies, similarity)

    # Display recommended movies
    st.subheader("Recommended Movies")
    num_movies = len(recommended_movies)
    cols = st.columns(num_movies)
    for i in range(num_movies):
        col = cols[i]
        col.header(recommended_movies[i])
        if recommended_movie_posters[i]:
            image = Image.open(requests.get(recommended_movie_posters[i], stream=True).raw)
            col.image(image, use_column_width=True)
        else:
            col.markdown("*No Poster Available*")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'>Project by Ayush</p>", unsafe_allow_html=True)
