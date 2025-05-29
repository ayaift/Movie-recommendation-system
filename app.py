<<<<<<< HEAD
'''
Author: Ayaift
Email: ayaift722@gmail.com
'''
import base64
import pickle
import numpy as np
import streamlit as st
import requests
import os
import random

# Session state variables for history, likes, and dislikes
if 'history' not in st.session_state:
    st.session_state.history = []
if 'liked_movies' not in st.session_state:
    st.session_state.liked_movies = set()
if 'disliked_movies' not in st.session_state:
    st.session_state.disliked_movies = set()

# Fetch poster using TMDB
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', None)
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://via.placeholder.com/150"

# Recommend function with dislike filtering
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:]:
        movie_id = movies.iloc[i[0]]['movie_id']
        title = movies.iloc[i[0]].title
        if title not in st.session_state['disliked_movies']:
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(title)
        if len(recommended_movie_names) == 5:
            break
    return recommended_movie_names, recommended_movie_posters

# App title
st.markdown("""
    <h1 style='color: white; font-weight: bold;'>Your best movie Recommender</h1>
""", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('dataset/savedmodels/movie_list.pkl','rb'))
similarity = pickle.load(open('dataset/savedmodels/similarity.pkl','rb'))
movie_list = movies['title'].values
st.markdown("<strong style='color:white;'>Type or select a movie from your choice</strong>", unsafe_allow_html=True)
selected_movie = st.selectbox("", movie_list, format_func=str)

colA, colB = st.columns(2)
with colA:
    see_recs = st.button('### See Recommendations')
with colB:
    choose_for_me = st.button("🎲 Choose for me")

if see_recs:
    movie_to_recommend = selected_movie
    st.session_state.history.append(movie_to_recommend)
    recommended_movie_names, recommended_movie_posters = recommend(movie_to_recommend)

    st.markdown(f"<h3 style='color: white;'>Recommendations based on: <strong>{movie_to_recommend}</strong></h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx >= len(recommended_movie_names):
            continue
        name = recommended_movie_names[idx]
        poster = recommended_movie_posters[idx]
        with col:
            st.markdown(f"<strong style='color: white;'>{name}</strong>", unsafe_allow_html=True)
            st.image(poster)
            subcol1, subcol2 = st.columns([1, 1])
            with subcol1:
                if st.button("👍", key=f"like_{name}"):
                    st.session_state['liked_movies'].add(name)
                    st.success("You liked this movie.")
            with subcol2:
                if st.button("👎", key=f"dislike_{name}"):
                    st.session_state['disliked_movies'].add(name)
                    del recommended_movie_names[idx]
                    del recommended_movie_posters[idx]
                    new_names, new_posters = recommend(movie_to_recommend)
                    for new_name, new_poster in zip(new_names, new_posters):
                        if new_name not in recommended_movie_names:
                            recommended_movie_names.insert(idx, new_name)
                            recommended_movie_posters.insert(idx, new_poster)
                            break
                    st.experimental_rerun()

elif choose_for_me:
    if st.session_state.history:
        base_movie = random.choice(st.session_state.history)
        recommended_movie_names, recommended_movie_posters = recommend(base_movie)
        pick_index = random.randint(0, min(4, len(recommended_movie_names)-1))
        surprise_movie = recommended_movie_names[pick_index]
        surprise_poster = recommended_movie_posters[pick_index]

        st.markdown(f"<h3 style='color: white;'>Based on your last preferences, we chose: <strong>{surprise_movie}</strong></h3>", unsafe_allow_html=True)
        st.image(surprise_poster)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍", key=f"like_surprise_{surprise_movie}"):
                st.session_state['liked_movies'].add(surprise_movie)
                st.success("You liked this movie.")
        with col2:
            if st.button("👎", key=f"dislike_surprise_{surprise_movie}"):
                st.session_state['disliked_movies'].add(surprise_movie)
                st.warning("We'll avoid similar movies next time.")
    else:
        st.markdown("""
            <span style='color: white; font-weight: bold;'>You need to see at least one recommendation first before we can choose for you.</span>
        """, unsafe_allow_html=True)

# Background setup

def set_background(image_file='bg.jpg'):
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

set_background("bg.png")
=======
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
>>>>>>> 10391d473893b1cc2a96f82f2d349cc7cc3262bd
