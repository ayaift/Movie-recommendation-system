'''
Author: Ayaift
Email: ayaift722@gmail.com
'''
import base64
import pickle
import streamlit as st
import requests
import time
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Ajout: historique de likes/dislikes
if 'disliked_movies' not in st.session_state:
    st.session_state['disliked_movies'] = set()
if 'liked_movies' not in st.session_state:
    st.session_state['liked_movies'] = set()
if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = []
    
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_names, recommended_posters = [], []
    for i in distances[1:]:
        #fetch the movie poster
        movie_title = movies.iloc[i[0]].title
        if movie_title not in st.session_state['disliked_movies'] and movie_title != movie:
            recommended_names.append(movie_title)
            recommended_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
        if len(recommended_names) == 5:
            break
    return recommended_names, recommended_posters


st.markdown(
    "<h1 style='color: white; font-weight: bold;'>Your best movie Recommender</h1>",
    unsafe_allow_html=True
)
movies = pickle.load(open('datasett/savedmodels/movie_list.pkl','rb'))
similarity = pickle.load(open('datasett/savedmodels/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from your choice",
    movie_list
)

if st.button('See Recommendations'):
    names, posters = recommend(selected_movie)
    st.session_state['recommendations'] = list(zip(names, posters))

# Affichage des recommandations existantes
if st.session_state['recommendations']:
    cols = st.columns(5)
    for idx in range(len(st.session_state['recommendations'])):
        name, poster = st.session_state['recommendations'][idx]
        with cols[idx]:
            st.text(name)
            st.image(poster)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key=f"like_{name}"):
                    st.session_state['liked_movies'].add(name)
                    st.success("You liked this movie.")
            with col2:
                if st.button("👎", key=f"dislike_{name}"):
                    st.session_state['disliked_movies'].add(name)
                    del st.session_state['recommendations'][idx]
                    new_names, new_posters = recommend(selected_movie)
                    for new_name, new_poster in zip(new_names, new_posters):
                        if new_name not in [r[0] for r in st.session_state['recommendations']]:
                            st.session_state['recommendations'].insert(idx, (new_name, new_poster))
                            break
                    st.experimental_rerun()

import streamlit as st
import base64

def set_background(image_file='bg.jpg'):  # or bg.png if that's what you downloaded
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    ext = image_file.split('.')[-1]

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/{ext};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)
set_background("bg.png")  # or "bg.png" depending on your file
