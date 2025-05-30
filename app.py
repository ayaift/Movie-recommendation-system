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

# Session State Initialization
if 'history' not in st.session_state:
    st.session_state.history = []
if 'liked_movies' not in st.session_state:
    st.session_state.liked_movies = set()
if 'disliked_movies' not in st.session_state:
    st.session_state.disliked_movies = set()
if 'already_seen_movies' not in st.session_state:
    st.session_state.already_seen_movies = set()
if 'current_recommendations' not in st.session_state:
    st.session_state.current_recommendations = []
if 'current_posters' not in st.session_state:
    st.session_state.current_posters = []
if 'selected_base_movie' not in st.session_state:
    st.session_state.selected_base_movie = None
if 'surprise_pick' not in st.session_state:
    st.session_state.surprise_pick = None
if 'surprise_poster' not in st.session_state:
    st.session_state.surprise_poster = None

# Fetch poster from TMDB API
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

# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:]:
        title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id
        if title not in st.session_state['disliked_movies']:
            recommended_movie_names.append(title)
            recommended_movie_posters.append(fetch_poster(movie_id))
        if len(recommended_movie_names) == 5:
            break
    return recommended_movie_names, recommended_movie_posters

# App Interface
st.markdown("""<h1 style='color: white; font-weight: bold;'>Your best movie Recommender</h1>""", unsafe_allow_html=True)

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

# SEE RECOMMENDATIONS
if see_recs:
    movie_to_recommend = selected_movie

    if movie_to_recommend not in st.session_state.history:
        st.session_state.history.append(movie_to_recommend)

    recommended_movie_names, recommended_movie_posters = recommend(movie_to_recommend)

    st.session_state.current_recommendations = recommended_movie_names
    st.session_state.current_posters = recommended_movie_posters
    st.session_state.selected_base_movie = movie_to_recommend
    st.session_state.surprise_pick = None
    st.session_state.surprise_poster = None

elif choose_for_me:
    if st.session_state.history:
        for _ in range(10):
            base_movie = random.choice(st.session_state.history)
            recommendations, posters = recommend(base_movie)
            for name, poster in zip(recommendations, posters):
                if name not in st.session_state.already_seen_movies:
                    st.session_state.surprise_pick = name
                    st.session_state.surprise_poster = poster
                    st.session_state.selected_base_movie = base_movie
                    break
            if st.session_state.surprise_pick:
                break

        st.session_state.current_recommendations = []
        st.session_state.current_posters = []
    else:
        st.markdown("<span style='color: white; font-weight: bold;'>You need to see at least one recommendation first before we can choose for you.</span>", unsafe_allow_html=True)

# DISPLAY SURPRISE PICK
if st.session_state.surprise_pick:
    st.markdown(f"<h3 style='color: white;'>Based on your last preferences, we chose: <strong>{st.session_state.surprise_pick}</strong></h3>", unsafe_allow_html=True)
    st.image(st.session_state.surprise_poster)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍", key=f"like_surprise_{st.session_state.surprise_pick}"):
            st.session_state['liked_movies'].add(st.session_state.surprise_pick)
            st.success("You liked this movie.")
    with col2:
        if st.button("👎", key=f"dislike_surprise_{st.session_state.surprise_pick}"):
            st.session_state['disliked_movies'].add(st.session_state.surprise_pick)
            st.warning("We'll avoid similar movies next time.")
            st.session_state.surprise_pick = None
            st.session_state.surprise_poster = None
            st.experimental_rerun()

    if st.button("Already seen", key=f"seen_surprise_{st.session_state.surprise_pick}"):
        st.session_state['already_seen_movies'].add(st.session_state.surprise_pick)
        st.info("Marked as already seen.")
        st.session_state.surprise_pick = None
        st.session_state.surprise_poster = None
        st.experimental_rerun()

# DISPLAY NORMAL RECOMMENDATIONS
if st.session_state.get("current_recommendations"):
    st.markdown(f"<h3 style='color: white;'>Recommendations based on: <strong>{st.session_state.selected_base_movie}</strong></h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx >= len(st.session_state.current_recommendations):
            continue
        name = st.session_state.current_recommendations[idx]
        poster = st.session_state.current_posters[idx]
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
                    new_names, new_posters = recommend(st.session_state.selected_base_movie)
                    for new_name, new_poster in zip(new_names, new_posters):
                        if new_name not in st.session_state.current_recommendations:
                            st.session_state.current_recommendations[idx] = new_name
                            st.session_state.current_posters[idx] = new_poster
                            break
                    st.experimental_rerun()

            if st.button("Already seen", key=f"seen_{name}"):
                st.session_state['already_seen_movies'].add(name)
                st.info("Marked as already seen.")


# Background Setup
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
