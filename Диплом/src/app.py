import os
import streamlit as st
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys
from PIL import Image # доб 

TOP_K = 5

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")  # раскомментировали"
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)      # раскомментировали"

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)

st.sidebar.title ("Recommendation Service")
st.sidebar.info("""Data Scientist, Project 14
       commando@student.21-school.ru""")

st.sidebar.title ("Работа сервиса")
st.sidebar.info("""
    Самые близкие фильмы по описанию из выбранного. \n

    Фильм 🔥- обязательный параметр;  
    Жанр - необязательный параметр,
    можешь выбрать несколько;  
    Режиссер 🤖 - необязательный параметр,  
    введи и имя, и фамилию"""
    , icon="ℹ️")

poster = Image.open ("Barbie.jpg")
st.image(poster, width = 700)

st.markdown(
    # "<h1 style='text-align: center; color: black;'>Movie Recommender Service</h1>",
    "<h1 style='text-align: center; color: darkcyan;'>сервис  рекомендаций  фильмов</h1>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "Фильм:",
    recsys.get_title()    
)





selected_genre = st.multiselect(
    "Выбери жанр фильма (один или несколько):",
    list(recsys.get_genres())
)

selected_director = st.text_input("Режиссер ") #

if st.button('РЕКОМЕНДОВАТЬ'):
    st.write("Рекомендации: ")
    recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K, genres=selected_genre, director=selected_director)
    recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
    if recommended_movie_names:
        columns = st.columns(TOP_K)
        for index in range(min(len(recommended_movie_names), TOP_K)):
            with columns[index]:
                st.image(recommended_movie_posters[index])
                st.subheader(recommended_movie_names[index])

    else:
        st.write("""Фильмы по заданным критериям не обнаружены""")
        

