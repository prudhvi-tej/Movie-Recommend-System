import streamlit as st
import pickle
import pandas as pd
import requests
from time import sleep

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d75b84c8081c0ade676ff8af7e700fa5&language=en-US'
    for attempt in range(10):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            sleep(2)
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = simi[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommend_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommend_posters
new_df=pickle.load(open("movies.pkl",'rb'))
movies_list=new_df['title'].values
movies_dict=pickle.load(open("movies.pkl",'rb'))
simi=pickle.load(open("simi.pkl",'rb'))
movies=pd.DataFrame(movies_dict)
st.title("Movie Recommendation System")
movie_name=st.selectbox(
    "What Movies do you like to see",movies['title'].values
)
if st.button("Recommend"):
    names,posters=recommend(movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])






